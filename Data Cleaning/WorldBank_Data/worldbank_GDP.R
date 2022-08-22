## this code assumes file is in excel format.
## pls download the relevant data sets from https://data.worldbank.org
## the csv example used in this code is embedded in the folder
## trying to extract GDP of countries from 2000 to 2015

getwd()    ## check your working dir
setwd("<insert directory here>")   ## set wd to where the excel file is downloaded

file_name = ""  ## insert file name
install.packages("readxl")    ## install if not alr installed
library("readxl")

df = read_excel(file_name)
View(df)  ## shows the data

## drop rows without country name
## name of col you want to remove NA values:
df2 = df[!is.na(df$`Country Name`),] 

## change string year format into shorter int format

year = sapply(names(df2)[5:20],
              function(x) {substr(x,1,4)})
names(year) = NULL
names(df2)[5:20] = years

series_code = "NY.GDP.PCAP.CD"
country = "United Kingdom"

df3 = df2[(df2$`Series Code` == series_code) &
          (df2$`Country Name` == country), 5:20]
View(df3)

GDP_pc = as.vector(df3[1,])   ## flattening vector
nm = as.vector(names(GDP_pc))
plot(nm, GDP_pc, type = 'b', col = 'navy', main = country,
     xlab = 'Year', ylab = 'GDP Per Capita')
