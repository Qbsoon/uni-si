import os
import sys
from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import easyocr
from PyQt6.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
	QTabWidget, QFileDialog, QSplitter, QDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from tqdm import tqdm

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class CardProcessor:
	def __init__(self):
		self.detection_model = YOLO('runs/detect/person_entry_model5/weights/best.pt')
		self.split_model = YOLO('runs/detect/split_image_id_model/weights/best.pt')
		self.rotation_model = YOLO('runs/pose/image_rotation_model3/weights/best.pt')

		self.debug_ocr_path = Path("debug_ocr_images")
		self.debug_ocr_path.mkdir(exist_ok=True)
		self.ocr_debug_counter = 0

		self.e_ocr = easyocr.Reader(['en'])

	def process_card(self, card_path):
		card = cv2.imread(card_path)

		pair_regions = self.detection_model.predict(source=card_path, save=False, conf=0.25, imgsz=1024, verbose=False)
		if not pair_regions or len(pair_regions) == 0:
			print(f"No regions detected in {card_path}.")
			return []

		print(f"Found {len(pair_regions)} image-id pair regions.")

		boxes = pair_regions[0].boxes.xywhn.cpu().numpy()

		results = []

		for i, box in enumerate(boxes):
			crop_box = self.extract_crop(card, box)

			split_regions = self.split_model.predict(source=crop_box, save=False, conf=0.25, imgsz=320, verbose=False)

			split_boxes = split_regions[0].boxes.xywhn.cpu().numpy()

			image_crop = self.extract_crop(crop_box, split_boxes[0])
			id_crop = self.extract_crop(crop_box, split_boxes[1])

			rotated_image = self.correct_orientation(image_crop)

			id = self.extract_id(id_crop)

			results.append({
				'id': id,
				'rotated_crop': rotated_image,
				'source_card': Path(card_path).name,
				'region_idx': i,
				'region': box
			})

		return results

	def extract_id(self, region):
		try:
			region = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)

			result = self.e_ocr.readtext(region, detail=0)
			if result:
				prediction = int(result[0]) if result[0].isdigit() else 0
			else:
				prediction = 0
		except Exception as e:
			print(f"Error extracting ID: {e}")
			return "unknown"

		return prediction

	def crop_image_from_prediction(self, card, prediction):
		if len(prediction.keypoints.xy) == 0:
			raise ValueError("Brak keypointów w predykcji")

		keypoints = prediction.keypoints.xy[0].cpu().numpy()

		if keypoints.shape[0] != 4:
			raise ValueError(f"Spodziewano się 4 punktów, a znaleziono {keypoints.shape[0]}")
		
		keypoints = keypoints.astype("float32")

		width = int(np.linalg.norm(keypoints[1] - keypoints[0]))
		height = int(np.linalg.norm(keypoints[3] - keypoints[0]))

		dst_pts = np.array([
			[0, 0],
			[width - 1, 0],
			[width - 1, height - 1],
			[0, height - 1]
		], dtype="float32")

		M = cv2.getPerspectiveTransform(keypoints, dst_pts)
		warped = cv2.warpPerspective(card, M, (width, height))

		return warped

	def correct_orientation(self, crop):
		rotation = self.rotation_model.predict(source=crop, save=False, conf=0.25, imgsz=416, verbose=False)
		rotated = self.crop_image_from_prediction(crop, rotation[0])
		return rotated

	def rotate_image(self, image, angle):
		(h, w) = image.shape[:2]
		center = (w // 2, h // 2)

		M = cv2.getRotationMatrix2D(center, -angle, 1.0)
		rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
		return rotated

	def extract_crop(self, card, region):
		card_h, card_w = card.shape[:2]

		region_x, region_y, region_w, region_h = region
		x_min = int((region_x - region_w / 2) * card_w)
		x_max = int((region_x + region_w / 2) * card_w)
		y_min = int((region_y - region_h / 2) * card_h)
		y_max = int((region_y + region_h / 2) * card_h)

		crop = card[y_min:y_max, x_min:x_max]
		return crop


def process_cards(input_dir, output_dir):
	processor = CardProcessor()

	input_path = Path(input_dir)
	output_path = Path(output_dir)
	output_path.mkdir(exist_ok=True)

	all_images_info = []
	images = []

	if os.path.isdir(input_dir):
		images = list(input_path.glob('*.jpg'))
	else:
		images = [input_path]
	with tqdm(total=len(images), desc="Processing images", unit="image") as img_bar:
		for image_file in images:
			clear_terminal()
			print(f"Processing {image_file.name}...")
			img_bar.update(1)
			img_bar.refresh()
			results = processor.process_card(str(image_file))

			for result in results:
				id = result['id']
				if id in ["ID_NOT_FOUND", "ID_NOT_DETECTED", "OCR_ERROR"]:
					filename = f"unknown_{result['source_card']}_{result['region_idx']}.jpg"
				else:
					filename = f"{id}.jpg"

				output_file = output_path / filename

				counter = 1
				while output_file.exists():
					if id in ["ID_NOT_FOUND", "ID_NOT_DETECTED", "OCR_ERROR"]:
						filename = f"unknown_{result['source_card']}_{result['region_idx']}_{counter}.jpg"
					else:
						filename = f"{id}_{counter}.jpg"
					output_file = output_path / filename
					counter += 1

				cv2.imwrite(str(output_file), result['rotated_crop'])

				all_images_info.append({
					'id': result['id'],
					'filepath': str(output_file),
					'source_card': result['source_card'],
					'region_idx': result['region_idx'],
					'region_x': result['region'][0],
					'region_y': result['region'][1],
					'region_w': result['region'][2],
					'region_h': result['region'][3],
				})

				print(f"  Saved: {filename} (ID: {result['id']})")

	if all_images_info:
		df = pd.DataFrame(all_images_info)
		df.to_csv(output_path / 'images_info.csv', index=False)

		print(f"\nProcessing complete!")
		print(f"Total images saved: {len(all_images_info)}")
		print(f"All images saved to: {output_path}")
		print(f"Image info saved to: {output_path / 'all_images.csv'}")
		return df
	return all_images_info



class WorkerThread(QThread):
	result_ready = pyqtSignal(pd.DataFrame, pd.DataFrame)

	def __init__(self, csv_path, input_path, output_path):
		super().__init__()
		self.csv_path = csv_path
		self.input_path = input_path
		self.output_path = output_path
		self._is_running = True

	def run(self):
		self._is_running = True
		df = pd.DataFrame()
		try:
			df = pd.read_csv(self.csv_path)
			df['id'] = df['id'].astype(str)
		except Exception as e:
			print(f"Nie udało się wczytać CSV: {e}")

		results = []
		try:
			results = process_cards(self.input_path, self.output_path)
			results['id'] = results['id'].astype(str)
			print(f"Przetworzono {len(results)} kart.")
		except Exception as e:
			print(f"Nie udało się przetworzyć kart: {e}")

		result_ids = set(results['id'].str.strip())
		df_ids = set(df['id'].str.strip())
		unknown_ids = result_ids - df_ids
		for unknown_id in unknown_ids:
			new_row = {col: ("unknown" if col != "id" else unknown_id) for col in df.columns}
			df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

		df_filtered = df[df['id'].isin(result_ids)].reset_index(drop=True)

		self.result_ready.emit(results, df_filtered)
		if not self._is_running:
			return

	def stop(self):
		self._is_running = False


class ProcessingDialog(QDialog):
	cancel_requested = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.setWindowTitle("Przetwarzanie...")
		self.setModal(True)
		layout = QVBoxLayout()
		layout.setSpacing(10)
		layout.addWidget(QLabel("Przetwarzanie..."))
		self.setLayout(layout)


class ImageViewer(QWidget):
	def __init__(self):
		super().__init__()
		self.df = pd.DataFrame()
		self.current_id = None

		layout = QVBoxLayout()
		layout.setSpacing(8)
		self.image_label = QLabel()
		self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(self.image_label, stretch=1)

		nav_layout = QHBoxLayout()
		self.first_btn = QPushButton("|<")
		self.prev_btn = QPushButton("<")
		self.next_btn = QPushButton(">")
		self.last_btn = QPushButton("|>")
		self.goto_input = QLineEdit()
		self.goto_input.setPlaceholderText("Go to ID")
		self.goto_input.setFixedWidth(80)
		nav_layout.addWidget(self.first_btn)
		nav_layout.addWidget(self.prev_btn)
		nav_layout.addWidget(self.goto_input)
		nav_layout.addWidget(self.next_btn)
		nav_layout.addWidget(self.last_btn)
		layout.addLayout(nav_layout)

		self.info_label = QLabel("")
		layout.addWidget(self.info_label)

		self.setLayout(layout)

		self.first_btn.clicked.connect(self.show_first)
		self.prev_btn.clicked.connect(self.show_prev)
		self.next_btn.clicked.connect(self.show_next)
		self.last_btn.clicked.connect(self.show_last)
		self.goto_input.returnPressed.connect(self.goto_id)

	def update_images(self, results_df, info_df):
		self.df = results_df.merge(info_df, on="id", how="left")
		self.current_id = self.df.iloc[0]['id']
		self.show_image()

	def show_image(self):
		row = self.df[self.df['id'] == self.current_id].iloc[0]
		pixmap = QPixmap(row['filepath'])
		self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
		info_text = f"ID: {row['id']}  Name: {row['name']}  Surname: {row['surname']}"
		self.info_label.setText(info_text)

	def show_first(self):
		self.current_id = self.df.iloc[0]['id']
		self.show_image()

	def show_last(self):
		self.current_id = self.df.iloc[-1]['id']
		self.show_image()

	def show_next(self):
		ids = self.df['id'].tolist()
		idx = ids.index(self.current_id)
		if idx + 1 < len(ids):
			self.current_id = ids[idx + 1]
			self.show_image()

	def show_prev(self):
		ids = self.df['id'].tolist()
		idx = ids.index(self.current_id)
		if idx - 1 >= 0:
			self.current_id = ids[idx - 1]
			self.show_image()

	def goto_id(self):
		target_id = self.goto_input.text().strip()
		matches = self.df[self.df['id'].astype(str) == target_id]
		if not matches.empty:
			self.current_id = matches.iloc[0]['id']
			self.show_image()


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Image Processor")
		main_layout = QHBoxLayout()

		splitter = QSplitter(Qt.Orientation.Horizontal)
		main_layout.addWidget(splitter)

		# Left side
		self.tabs = QTabWidget()
		self.init_tab1()
		self.init_tab2()
		splitter.addWidget(self.tabs)

		# Right side (image viewer)
		self.viewer = ImageViewer()
		self.viewer.setMinimumWidth(400)
		splitter.addWidget(self.viewer)
		splitter.setStretchFactor(0, 4)
		splitter.setStretchFactor(1, 5)

		self.setLayout(main_layout)

	def init_tab1(self):
		widget = QWidget()
		layout = QVBoxLayout()
		layout.setSpacing(6)

		self.csv_file1 = QLineEdit()
		browse_csv1 = QPushButton("Wybierz CSV")
		browse_csv1.clicked.connect(lambda: self.browse_file(target=self.csv_file1))
		row0 = QHBoxLayout()
		row0.addWidget(self.csv_file1)
		row0.addWidget(browse_csv1)
		layout.addLayout(row0)

		self.input_dir1 = QLineEdit()
		browse_btn1 = QPushButton("Przeglądaj")
		browse_btn1.clicked.connect(lambda: self.browse_directory(target=self.input_dir1))
		row1 = QHBoxLayout()
		row1.addWidget(self.input_dir1)
		row1.addWidget(browse_btn1)
		layout.addLayout(row1)

		self.output_dir1 = QLineEdit()
		browse_out1 = QPushButton("Przeglądaj")
		browse_out1.clicked.connect(lambda: self.browse_directory(target=self.output_dir1))
		row2 = QHBoxLayout()
		row2.addWidget(self.output_dir1)
		row2.addWidget(browse_out1)
		layout.addLayout(row2)

		extract_btn = QPushButton("Extract")
		extract_btn.clicked.connect(lambda: self.start_processing(self.csv_file1.text(), self.input_dir1.text(), self.output_dir1.text()))
		layout.addWidget(extract_btn)
		layout.addStretch()
		widget.setLayout(layout)
		self.tabs.addTab(widget, "From Folder")

	def init_tab2(self):
		widget = QWidget()
		layout = QVBoxLayout()
		layout.setSpacing(6)

		self.csv_file2 = QLineEdit()
		browse_csv2 = QPushButton("Wybierz CSV")
		browse_csv2.clicked.connect(lambda: self.browse_file(target=self.csv_file2))
		row0 = QHBoxLayout()
		row0.addWidget(self.csv_file2)
		row0.addWidget(browse_csv2)
		layout.addLayout(row0)

		self.input_file2 = QLineEdit()
		browse_btn2 = QPushButton("Przeglądaj")
		browse_btn2.clicked.connect(lambda: self.browse_file(target=self.input_file2))
		row1 = QHBoxLayout()
		row1.addWidget(self.input_file2)
		row1.addWidget(browse_btn2)
		layout.addLayout(row1)

		self.output_dir2 = QLineEdit()
		browse_out2 = QPushButton("Przeglądaj")
		browse_out2.clicked.connect(lambda: self.browse_directory(target=self.output_dir2))
		row2 = QHBoxLayout()
		row2.addWidget(self.output_dir2)
		row2.addWidget(browse_out2)
		layout.addLayout(row2)

		extract_btn = QPushButton("Extract")
		extract_btn.clicked.connect(lambda: self.start_processing(self.csv_file2.text(), self.input_file2.text(), self.output_dir2.text()))
		layout.addWidget(extract_btn)
		layout.addStretch()
		widget.setLayout(layout)
		self.tabs.addTab(widget, "From File")

	def browse_directory(self, target):
		dir_path = QFileDialog.getExistingDirectory(self, "Wybierz katalog")
		target.setText(dir_path)

	def browse_file(self, target):
		file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik")
		target.setText(file_path)

	def start_processing(self, csv_path, input_path, output_path):
		self.dialog = ProcessingDialog()
		self.worker = WorkerThread(csv_path, input_path, output_path)
		self.worker.result_ready.connect(self.on_result_ready)
		self.dialog.cancel_requested.connect(self.worker.stop)
		self.worker.start()
		self.dialog.exec()

	def on_result_ready(self, images, df):
		print("on_result_ready called")
		self.viewer.update_images(images, df)
		self.dialog.accept()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.resize(1000, 600)
	window.show()
	sys.exit(app.exec())