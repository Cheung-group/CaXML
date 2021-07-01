library(ggplot2)
library(stringr)
library(reshape2)
library(dplyr)
setwd('C:/Users/Pengzhi/Downloads')
X776ProbabilityGraph <- read.csv(file = '776ProbabilityGraph.csv')
Residue <- X776ProbabilityGraph$Residue
y <- factor(Residue,levels = c("1","2","3","4","5","6","7","8","9","10","11","12","15","16"))
names(X776ProbabilityGraph)<-str_replace_all(names(X776ProbabilityGraph), c(" " = "." , "," = "" ))

betweennesscentrality<-ggplot(X776ProbabilityGraph,aes(x = NormBetween, y = y))+
  geom_boxplot(fill='#348e9e', color="black")+
  labs(y= "Residue", x = "Betweenness Centrality")+
  scale_y_discrete(label = c("1","2","3","4","5","6","7","8","9","10","11","12","Ca","Water"))+
  theme_classic()


clustering <- ggplot(X776ProbabilityGraph,aes(x = clustering, y = y))+
  geom_boxplot(fill='#A4A4A4', color="black")+
  labs(y= "Residue", x = "Clustering Coefficient")+
  scale_y_discrete(label = c("1","2","3","4","5","6","7","8","9","10","11","12","Ca","Water"))+
  theme_classic()

degreeFrame <- X776ProbabilityGraph[c("Degree","Weighted.Degree","Residue")]
degreeFrame.m <- melt(degreeFrame)
degrees <- ggplot(degreeFrame.m,aes(x = value, y = Residue))+
  geom_boxplot(aes(fill = variable), color="black")+
  labs(y= "Residue", x = "Degree")+
  scale_y_discrete(label = c("1","2","3","4","5","6","7","8","9","10","11","12","Ca","Water"))+
  scale_x_continuous(breaks=c(1,2,3,4,5,6,7,8,9,10,11,12))+
  theme_classic()


weighteddegree <- ggplot(X776ProbabilityGraph,aes(x = Weighted.Degree, y = y))+
  geom_boxplot(fill='#A4A4A4', color="black")+
  labs(y= "Residue", x = "Weighted Degree")+
  scale_y_discrete(label = c("1","2","3","4","5","6","7","8","9","10","11","12","Ca","Water"))+
  theme_classic()+
  theme( )

