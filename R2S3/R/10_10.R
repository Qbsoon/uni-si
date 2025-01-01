temp <- c(20,21,17,19,22,18,16)
temp
dni <- c('Pon','Wt','Śr','Czw',"Pt",'Sb','Nd')
dni
names(temp) <- dni
temp
x=c(1,2,3)
names(x)<-c('a','s','d')
x
names(x)
x['a']
x[x>2]
2^5
ceny_akcji<-c(23,27,23,21,34)
names(ceny_akcji)<-c("Pn","Wt","Śr","Czw","Pt")
ceny_akcji

mean(ceny_akcji)
ponad23<-ceny_akcji>23
ponad23

ceny_akcji[ponad23]

max(ceny_akcji)

names(ceny_akcji)[ceny_akcji==max(ceny_akcji)]

