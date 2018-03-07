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
       if z(m,n)<3000
          z(m,n)=11.11;
       end
       
    end
end 


%sareamatrix=zeros(33,33);
%生成73*70的面积矩矩阵,矩阵数据坐标为（ax,ay）,(ax,ay)上下左右边线分别为32ay+1,32ay-31,32ax-31,32ax+1;

sarea=zeros(72,69);

% for bucg=1:1:26
%     z(:,2775+bucg)=0;
% end
% 
% for bucg=1:1:8
%     z(2913+bucg,:)=0;
% end



for i=1:1:72
    for j=1:1:69
       %sareamatrix=zeros(33,33);
       sareamatrix=z(i*40-39:i*40+1,j*40-39:j*40+1);
       numx1=0;numx2=0;
       numx3=0;numx4=0;numx5=0;
     for num=1:1:41
       numx1=length(find(sareamatrix(num,:)==11.11))+numx1;
     end
       numx2=length(find(sareamatrix(1,:)==11.11));
       numx3=length(find(sareamatrix(33,:)==11.11));
       numx4=length(find(sareamatrix(:,1)==11.11));
       numx5=length(find(sareamatrix(:,33)==11.11));
       sarea(j,i)=numx1*38.2*38.2-(numx2+numx3+numx4+numx5)*38.2*38.2*0.5;
       if  sarea(j,i)~=0
          z(i*40-39:i*40+1,j*40-39:j*40+1)=zeros(41,41); 
       end
    end
end

for n=1:1:2775
    for m=1:1:2913
       if z(m,n)<3000
          z(m,n)=0;
       end
       
    end
end 

figure,contourf(xi,yi,z) %等高线图
%xlim([59000 89000 46000 76000])
colorbar
hold on;





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