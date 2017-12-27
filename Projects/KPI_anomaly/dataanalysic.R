library(xts)
library(lubridate)
library(dplyr)

train<-read.csv("../../dataset/anomaly_detection_1/train.csv")
submit<-read.csv("../../dataset/anomaly_detection_1/test_dataset.csv")
submit$label<-0
KPI_IDs<-unique(train$KPI.ID)

#基于一个简单的规则，根据观察，周期主要是一天一天的，所以把每天某时刻某分钟单独提取出来比较，偏离比较大的视为异常点
tmp_line1<-train[which(train$KPI.ID == KPI_IDs[27]),]
tmp_line2<-submit[which(submit$KPI.ID == KPI_IDs[27]),]
names(tmp_line1)<-c("id","timestamp","value","label")
names(tmp_line2)<-c("id","timestamp","value","label")
tmp_line<-rbind(tmp_line1,tmp_line2)
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
#samples$value<-log(samples$value+1)
group<-group_by(samples,date)
sta1<-summarise(group,mean=mean(value),sd=sd(value))
samples<-merge(samples,sta1,by.x = "date",by.y = "date")
samples$value<-(samples$value-samples$mean)/samples$sd
group<-group_by(samples,hour,minute)
sta2<-summarise(group,median=median(value,na.rm = T))
samples<-merge(samples,sta2,by.x = c("hour","minute"),by.y = c("hour","minute"))
samples$diff1<-abs(samples$median-samples$value)
samples$predict<-0
samples1<-merge(tmp_line1[,c(1,2)],samples,by.x=c("id","timestamp"),by.y = c("id","timestamp"),all.x = T)
samples2<-merge(tmp_line2[,c(1,2)],samples,by.x=c("id","timestamp"),by.y = c("id","timestamp"),all.x = T)
write.csv(samples1,"./samples/samples1.csv",row.names = F,quote = F)

samples2[which(samples2$diff1>0.9),"label"]<-1
write.csv(samples2[,c("id","timestamp","label")],"./results/result_27.csv",row.names = F,quote = F)

#计算结果
getRecallandPre<-function(tmp_line,gap){
  sum1<-sum(tmp_line$label)
  sum2<-length(tmp_line[which(tmp_line$diff1>gap),"label"])
  get1<-sum(tmp_line[which(tmp_line$diff1>gap),"label"])
  pre<-get1/sum2
  rec<-get1/sum1
  print(get1)
  print(sum2)
  print(pre)
  print(rec)
  f1<-2*pre*rec/(pre+rec)
  f1
}


#提交
filenames<-c("result_01.csv","result_02.csv","result_03.csv","result_04.csv","result_05.csv","result_06.csv","result_07.csv","result_08.csv","result_09.csv","result_10.csv","result_11.csv","result_12.csv","result_13.csv","result_14.csv","result_15.csv","result_16.csv","result_17.csv","result_18.csv","result_19.csv","result_20.csv","result_21.csv","result_22.csv","result_23.csv","result_24.csv","result_25.csv","result_26.csv","result_27.csv")
pdata<-NULL
for(i in filenames){
  data<-read.csv(paste("./results/",i,sep = ""))
  pdata<-rbind(pdata,data)
}