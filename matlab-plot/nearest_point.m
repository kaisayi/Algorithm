function  [pointx,pointy]=nearest_point([start_x,start_y],sarea_func(87,91))
    %寻找最近距离
distance_1_nearest=200000;
distance_2_nearest=200000;
    for i=1:1:91
        for j=1:1:87
            if sarea(i,j)~=0
                if distance_1(i,j)<distance_1_nearest
                    distance_1_nearest=distance_1(i,j);  %将最近的距离赋给distanc_1_nearest
                    N1=(i,j);                            %将该点的坐标赋给N1
                end
                if distance_2(i,j)<distance_2_nearest
                    distance_2_nearest=distance_2(i,j);  %将最近的距离赋给distanc_2_nearest
                    N2=(i,j);                            %将该点的坐标赋给N2
                end
            %elseif 
            end
        end
    end
end