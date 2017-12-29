train<-read.csv("../../dataset/anomaly_detection_1/train.csv")
submit<-read.csv("../../dataset/anomaly_detection_1/test_dataset.csv")
submit$label<-0
KPI_IDs<-unique(train$KPI.ID)

tmp_line<-train[which(train$KPI.ID == KPI_IDs[1]),]
names(tmp_line)<-c("id","timestamp","value","label")
tmp_line$datetime<-as.POSIXct(tmp_line$timestamp, origin="1970-01-01")
samples<-NULL
order<-1
for(i in 1:nrow(tmp_line)){
  samples$id[order]<-as.character(tmp_line[i,1])
  samples$timestamp[order]<-tmp_line[i,"timestamp"]
  samples$label[order]<-as.numeric(tmp_line[i,'label'])
  samples$hour[order]<-hour(tmp_line[i,"datetime"])
  samples$minute[order]<-as.integer(minute(tmp_line[i,"datetime"]))
  samples$value[order]<-tmp_line[i,"value"]
  samples$date[order]<-as.Date(tmp_line[i,"datetime"])
  order<-order+1
}
samples<-data.frame(samples)
group<-group_by(samples,hour,minute)
sta2<-summarise(group,median=median(value,na.rm = T))
samples<-merge(samples,sta2,by.x = c("hour","minute"),by.y = c("hour","minute"))
write.csv(samples[,c(3,4,6)],"./samples/samples_test.csv",row.names = F,quote = F)
samples[which(samples$label==1),"value"]<-samples[which(samples$label==1),"median"]
write.csv(samples[,c(3,4,6)],"./samples/samples_train.csv",row.names = F,quote = F)
