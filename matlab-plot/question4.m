clc
clear all

points=xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\2017年试题\A\附件2.xlsx');
for i=1:1:72
    pointx(i)=points(i,2)*1000;
    pointy(i)=points(i,3)*1000;
end

figure
plot(pointx,pointy,'.','markersize',20,'color','r');
hold on;
xlim([0 110000]);
ylim([0 140000]);
axis square

points2=xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\PPT图片\disk4.xlsx');
%plot(points2(:,1),points2(:,2),'.','markersize',20)

for m=1:1:55
    r=2500;
    theta=0:pi/50:2*pi;
    x=points2(m,1)*1000+r*cos(theta);
    y=points2(m,2)*1000+r*sin(theta);
    plot(x,y,'-','markersize',2,'color','g','linewidth',2);
    axis([0 110000  0 140000]); 
    text(points2(m,1)*1000+100,points2(m,2)*1000+100,num2str(m),'color','k','fontSize',12);
    %scatter(x(i)*1000,y(i)*1000,10000,'filled')
    axis square;
    hold on
end 