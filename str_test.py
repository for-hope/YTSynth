str1="Hello this is the first string, it will be used in this project"
str2 = "Hello this is string2 and i will not be used in this project"
str3=str1.split()
str4=str2.split()
str5=""
for i in range(0,len(str3)):
  if(str3[i]==str4[i]):     
    str5+=str3[i]
    str5+=" "
print(str5)