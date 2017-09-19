clc 
clear all
yi = 0: 38.2: 38.2*2912;
xi = 0: 38.2: 38.2*2774;

%doc  line %plot %scatter%xlsread
z = xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\2017年试题\A\附件1 区域高程数据.xlsx');
z=z';
%surf(x, y, z)
for n=1:1:2775
    for m=1:1:2913
       if z(m,n)<0
          z(m,n)=0;
       end
       
    end
end 
figure,contourf(xi,yi,z) %等高线图
%xlim([59000 89000 46000 76000])
colorbar
hold on;

% x0=[30.3,66.0,98.4,73.7,57.9,86.8,93.6];
% y0=[89.8,84.7,76.7,61.0,47.6,22.0,48.8];
% r=10000;
% for i=1:1:7
%     theta=0:pi/50:2*pi;
%     x=x0(i)*1000+r*cos(theta);
%     y=y0(i)*1000+r*sin(theta);
%     plot(x,y,'-',x0(i)*1000,y0(i)*1000,'.','markersize',2,'color','g','linewidth',2);
%     axis([0 111000 0 111200]); 
%     %scatter(x(i)*1000,y(i)*1000,10000,'filled')
%     axis square;
% end 
% hold on;

xh=110000;
yh=0;
plot(xh,yh,'.','markersize',25,'color','r');
axis([0 111000 0 111200]); 
axis square;
hold on

for i=1:1:75
    line([1,111000],[38.2*40*i,38.2*40*i],'linewidth',0.01,'color','k');
end
hold on 
 
for j=1:1:75
    line([38.2*40*j,38.2*40*j],[1,38.2*2912],'linewidth',0.01,'color','k');
end
hold on 


%figure,surfc(X,Y,Z)%三维曲面
%colorbar
%shading interp