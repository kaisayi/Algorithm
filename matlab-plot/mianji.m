clc 
clear all
yi = 0: 38.2: 38.2*2912;
xi = 0: 38.2: 38.2*2774;

%doc  plot %scatter%xlsread
z = xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\2017年试题\A\附件1 区域高程数据.xlsx');
z=z';
%surf(x, y, z)
for n=1:1:2775
    for m=1:1:2913
       if z(m,n)<3000
         z(m,n)=11.11;  
       end 
    end
end 

x0=[30.3,66.0,98.4,73.7,57.9,86.8,93.6];
y0=[89.8,84.7,76.7,61.0,47.6,22.0,48.8];

num0=0;
for i=1:1:7
    for m=1:1:2775
      for n=1:1:2913
          rr=((xi(m)-x0(i)*1000)^2+(yi(n)-y0(i)*1000)^2);
          if z(n,m)==11.11&rr<100000000
            num0=num0+1;
          end       
      end
    end
    Sarea(i)=38.2*38.2*num0;
    num0
    num0=0;
end
    
Sarea