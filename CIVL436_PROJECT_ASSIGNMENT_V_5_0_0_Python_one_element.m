%%%%%%%%%%%%%%%%%%%%% CIVL 436 PROJECT ASSIGNMENT %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%% TEAM 2: EMMA ROSE, JOSH BIAN, NED TAYLOR %%%%%%%%%%%%%%%%%%

%%%%%%%% PROGRAM INPUT DEFINITIONS:

%%% Member definition inputs:
% nodei  : vector containing the X and Y coordinates of node i
% nodej  : vector containing the X and Y coordinates of node j
% mapVector   : Vector defining how each members local DoFs correspond to
%               global DoFs
% supp_Vector : Vector that defines which global DoFs are restrained and
%               which are free
% TrussVector : Vector that defines which members are trusses and frames 
% num_Elements: Input the number of elements 
%
% Material property inputs:
% EVector: Vector containing each element's material's Young's modulus
% IVector: Vector containing each element's cross section's moment of 
%          inertia
% AVector: Vector containing each element's cross section's area
% AlphaVector: Vector containing each element's material's coefficient
%              of thermal expansion
%
%%% Loading condition inputs:
% Note : All element loading conditions are in local coordinates
% P    : applied point loads at locations along the element's local x
%        axis, where the first column is x and the second through fourth
%        columns are P in each direction xyz
% w    : distributed loads along the beam (w is 1 by 3, where each
%        element corresponds to the local coordinate system axis (xyz)
% specifiedDelta: specified displacements at all 6 element degrees of
%                 freedom, these are included in displacement results
% deltaT        : the applied change in temperature 
% shrinkStrain  : any applied shrinkage in units of strain (length/length)

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Enter Variables: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Member definitions: 
%List all elements below:
nodei1 = [0,0]; 
nodej1 = [3,3]; 
map1 = [1,2,3,4,5,6];

%nodei2 = [3,3]; 
%nodej2 = [3,5];
%map2 = [4,5,6,7,8,9];



%Note: Add or remove columns/rows to match the amount of elements
nodeCoordinates = {nodei1,nodej1};
mapVector = {map1}; 
supp_Vector = [1,1,1 , 1,1,1]; %1 = restrained DoF, 0 = Free DoF
TrussVector = [0 ; 0];                     %1 = truss member, 0 = frame member
num_Elements = 1; 

%Material and geometric property inputs:
%Note: Add or remove rows for each vector so that # of rows = # of elements
EVector = [220*10^9]; %(N/m) 
IVector = [0.00022]; %(m^4) 
AVector = [0.05]; %(m^2)
alphaVector = [12*10^-6 ]; %(1/C)

%Loading condition inputs
% Note: Add or remove columns/rows to match the amount of elements
PArray = {[1,5000,5000,5000]}; %[m,N,N,N]
wArray = {[1500,1500,1500]  }; %[N/m,N/m,N/m]
specifiedDeltaArray = {[0;0;0;0;0;0] }; %[m,m,m,m,m,m]
deltaT_Vector = [0];  %degrees C
shrinkStrainVector = [0]; %m/m


%Output1 = Rs_mapped    : A vector containing the reaction forces at 
%                         every fixed node in newtons(In Global DoFs) 
%Output2 = deltaf_mapped: A vector containing the displacements at every
%                         free node in meters(In Global DoFs))

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%Function begins - No further inputs required


Num_Nodes = size(nodeCoordinates)+1;%Counts the number of nodes based on input. 
num_DoFs = Num_Nodes(1,1)*3;%Counts the number of DoFs, based on number of nodes

GlobalForceVector = zeros(num_DoFs,1); %Creates a zeros vector to store mapped FEFs in the below for loop. Has columns equal to the # of DoF
GlobalspecifiedDeltaMapped = zeros(num_DoFs,1); %%Creates a zeros vector to store mapped FEFs in the below for loop. Has columns equal to the # of DoF


%Defines cells for each elements stiffness and force matrices
T = cell(num_Elements(1,1),1);
KLocal = cell(num_Elements(1,1),1);
FEFLocal = cell(num_Elements(1,1),1);
FEFGlobal = cell(num_Elements(1,1),1);

for i = 1:num_Elements(1,1)%Repeates the loop once for each element

T{i} = GetGlobalTransformationMatrix(nodeCoordinates{i,1},nodeCoordinates{i,2},TrussVector(i)); %Computes a local to global stiffness matrix for every element and stores them in an array
KLocal{i} = GetLocalStiffnessMatrix(nodeCoordinates{i,1},nodeCoordinates{i,2},EVector(i),IVector(i),AVector(i),TrussVector(i)); %Uses a function to get local stiffness matrices for every element and stores into an array
KGlobal{i} = T{i}*KLocal{i}*transpose(T{i}); %Computes global stiffness matrices for every element and stores them in an array

FEFLocal{i} = GetLocalFEFs(nodeCoordinates{i,1},nodeCoordinates{i,2},EVector(i),alphaVector(i),IVector(i),AVector(i),PArray{i},wArray{i},specifiedDeltaArray{i},deltaT_Vector(i),shrinkStrainVector(i)); %Uses function to get fixed end forces in local coordinates and stores them in an array
FEFGlobal{i} = T{i}*FEFLocal{i}; %Computes and stores all global FEF vectors into an array.

FEFElementMapped = zeros(num_DoFs(1,1),1); %Creates a zeros vector to temporarily store mapped FEFs in
FEFElementMapped(mapVector{i}) = FEFGlobal{i}; %Maps the FEFs (global coords) into the temporary force vector

specifiedDeltaMapped = zeros(num_DoFs(1,1),1); %Creates a zeros vector to temporarily store mapped specified displacements in
specifiedDeltaMapped(mapVector{i}) = specifiedDeltaArray{i}; %Maps the specified displacements into the temporary vector above

GlobalForceVector = GlobalForceVector + FEFElementMapped; %Adds each element's mapped force vector into one single vector

GlobalspecifiedDeltaMapped = GlobalspecifiedDeltaMapped + specifiedDeltaMapped; %Adds each element's specified displacements into 

end 

KStructure = GetStructureStiffnessMatrix(KGlobal,mapVector); %Uses a function to generate global structure stiffness matrix

%Below section is for partitioning
numberOfSupports = sum(supp_Vector); %Counts the number of fixed DoFs in the system
numberOfFreeDoFs = num_DoFs - numberOfSupports; %Counts the number of free DoFs in the system

supportLocations = zeros(1,num_DoFs); %Creates a zero vector with length equal to number of DoFs
freeLocations = zeros(1,num_DoFs); %Creates a zero vector with length equal to number of DoFs

for i = 1:num_DoFs %Repeats loop once for each DoF
    
    if supp_Vector(i) == 1 %The empty vector defined above gets assigned support locations based on user input. IE: supportLocations = [[0,2,0,0,5], in this system the user defined node 2 and 5 as fixed.
    supportLocations(1,i) = i; 
    end
    
    if supp_Vector(i) == 0 %Same as above, the empty vector defined above gets assigned free locations based on user input.
    freeLocations(1,i) = i;
    end
    
end

supportLocations = nonzeros(supportLocations); %Removes all zeros in the 'SupportLocations' vector, IE: [2,5]
freeLocations = nonzeros(freeLocations); %%Removes all zeros in the 'FreeLocations' vector

Kss = KStructure(supportLocations,supportLocations); %Assigns the fixed rows and fixed columns of KStructure to Kss
Ksf = KStructure(supportLocations,freeLocations); %Assigns the fixed rows and free columns of KStrucutre to Ksf
Kff = KStructure(freeLocations,freeLocations); %Assigns the free rows and free columns of KStrucutre to K
Kfs = KStructure(freeLocations,supportLocations); %Assigns the free rows and fixed columns of KStrucutre to Kss

FEFs = (GlobalForceVector(supportLocations)); %Defines a vector containing only FEFs at supports that arise from load conditions 
FEFf = (GlobalForceVector(freeLocations)); %Defines a vector that contains only FEFs at free DoFs that arise from load conditions

deltaf =((Kff)^-1*FEFf)*-1;%finds displacements at free DOFs, units are meters

Rs = (Ksf*deltaf+FEFs); %finds reactions at fixed DOFs, units are N

deltaf_mapped = zeros(num_DoFs,1); %Creates a zeros vector of equal size to the number of DoFs
deltaf_mapped(freeLocations) = deltaf; %Returns displacements of every node in the order the nodes were inputted
deltaf_mapped_total = deltaf_mapped + GlobalspecifiedDeltaMapped; %Adds the specified displacements and the deltaf_mapped for final displacement values

Rs_mapped = zeros(num_DoFs,1); %Creates a zeros vector of equal size to the number of DoFs
Rs_mapped(supportLocations) = Rs; %Returns reaction forces of every node in the order the nodes were inputted


%%%%%%%%%%%% The following four functions are used by the code above %%%%%%%%%%%%% 

%GetGlobalTransformationMatrix(nodei,nodej,Truss)
%GetLocalStiffnessMatrix(nodei,nodej,E,I,A,Truss)
%GetLocalFEFs(nodei,nodej,E,alpha,I,A,P,w,specifiedDelta,deltaT,shrinkStrain)
%GetStructureStiffnessMatrix(K,map)

function [output] = GetGlobalTransformationMatrix(nodei,nodej,Truss)
%Input of function is two nodes with X and Y coordinates as follows: ([Xi,Yi],[Xj,Yj])

%Creates two variables 'DeltaX' and 'DeltaY'to calculate the global horizontal displacement and global vertical displacement respectively
%Variables can be negative or positive
DeltaX = nodej(1,1) - nodei(1,1);
DeltaY = nodej(1,2) - nodei(1,2);

%The following 6 if statements account for any cases of nodei and nodej arrangements

if (DeltaX > 0) && (DeltaY >= 0)% For positive DeltaX and DeltaY (or DeltaY==0) (1st quadrant)
Theta = 2*pi - atan(DeltaY/DeltaX);
end

if (DeltaX < 0) && (DeltaY >= 0) % For Negative DetlaX and Positive DeltaY (or DeltaY==0) (2nd quadrant)
Theta = pi + atan(DeltaY/abs(DeltaX));
end

if (DeltaX < 0) && (DeltaY < 0) % For Negative DeltaX and DeltaY (3rd Quadrant)
Theta = pi - atan(abs(DeltaY)/abs(DeltaX));
end

if (DeltaX > 0) && (DeltaY < 0) % For Positive DeltaX and Negative DeltaY (4th quadrant)
Theta = atan(abs(DeltaY)/DeltaX);
end

if (DeltaX == 0) && (DeltaY > 0)% For when DeltaX == 0 and DeltaY > 0 (Element vertical and upwards)
    Theta = 3/2*pi;
end

if (DeltaX == 0) && (DeltaY < 0)% For when Delta == 0 and DeltaY < 0 (Elemtent vertical and downwards)
    Theta = 1/2*pi;
end


if (Truss == 1) %Truss == 1 is for truss members
    T = [cos(Theta),sin(Theta),0,0,0,0;-sin(Theta),cos(Theta),0,0,0,0;0,0,0,0,0,0;0,0,0,cos(Theta),sin(Theta),0;0,0,0,-sin(Theta),cos(Theta),0;0,0,0,0,0,0];
end

if (Truss == 0)
%Uses the angle 'Theta' (measured positive and CCW) to produce the coordinate transformation matrix of the given element
T = [cos(Theta),sin(Theta),0,0,0,0;-sin(Theta),cos(Theta),0,0,0,0;0,0,1,0,0,0;0,0,0,cos(Theta),sin(Theta),0;0,0,0,-sin(Theta),cos(Theta),0;0,0,0,0,0,1];
end

%Outputs the coordinate transformation matrix of the given element 
output = T;


end
% The above function takes any two node coordinates, calculates the angle of the element 
% between the given nodes relative to the global coordinate system and uses this angle to 
% create a global coordinate transformation matrix. 
% The above function works for any two inputted node coordinates.


function [output] = GetLocalStiffnessMatrix(nodei,nodej,E,I,A,Truss)

% Computes the horizontal and vertical component of the element and stores
% them in the variables deltaX and deltaY respectively
deltaX = nodej(1,1)- nodei(1,1);
deltaY = nodej(1,2) - nodei(1,2);

% Uses deltaX and deltaY to compute the elements length
L = sqrt(deltaX^2 + deltaY^2);

% For simplicity, each term within the stiffness matrix is calculated and 
% stored within a seperate variable (a,b,c, and d)
a = E*A/L;
b = 12*E*I/L^3;
c = 6*E*I/L^2;
d = 4*E*I/L;

% Formulates the local stiffness matrix as derived in problem 1 of HW2.
Klocal = [a,0,0,-a,0,0;0,b,c,0,-b,c;0,c,d,0,-c,d/2;-a,0,0,a,0,0;0,-b,-c,0,b,-c;0,c,d/2,0,-c,d];

if (Truss == 1)
    Klocal = [a,0,0,-a,0,0;0,0,0,0,0,0;0,0,0,0,0,0;-a,0,0,a,0,0;0,0,0,0,0,0;0,0,0,0,0,0];
end

% Outputs the local stiffness matrix of the given element
output = Klocal;

end
% The above function takes two node inputs along with the required section
% and material inputs. It computes the length of the element, and then
% uses the provided information to calculate all terms within the local
% stiffness matrix.


function [output] = GetLocalFEFs(nodei,nodej,E,alpha,I,A,P,w,specifiedDelta,deltaT,shrinkStrain)

DeltaX = nodej(1,1) - nodei(1,1); %Computes DeltaX between nodei and nodej
DeltaY = nodej(1,2) - nodei(1,2); %Computes DeltaY between nodei and nodej

L = sqrt(DeltaX.^2+DeltaY.^2); %Computes the length of the element using DeltaX and DeltaY

%This section of code creates a 6x1 vector representing local fixed end forces. It accounts for any applied loads in 
%the X and Y directions and adds the resulting FEFs to the vector.
Py = P(1,3);
Px = P(1,2);
a = P(1,1);
b = L-a;

FEFL = [-Px*b/L ; -Py*b.^2*(3*a+b)/L.^3 ; -Py*b.^2*a/L.^2 ; -Px*a/L ; -Py*a.^2*(b*3+a)/L.^3 ; Py*b*a.^2/L.^2];

%This section accounts for any applied moments in the z direction and addes them to the FEFL
M = P(1,4);
a = P(1,1);
b = L-a;

FEFL = FEFL + [0 ; 6*M*a*b/L.^3 ; M*b*(2*a-b)/L.^2 ; 0 ; -6*M*a*b/L.^3 ; M*a*(2*b-a)/L.^2 ];

%This section calculates FEFs from any distributed loads in the x,y, or z direction and adds them to FEFL
Wx = w(1,1);
Wy = w(1,2);
Wz = w(1,3);

FEFL = FEFL + [-Wx*L/2 ; -Wy*L/2 + Wz ; -Wy*L^2/12 ; -Wx*L/2 ; -Wy*L/2 - Wz; Wy*L^2/12];

%This section computes FEFs that result from temperature change and adds them to the FEFL using the equation P = DeltaL*E*A/L
FEFL = FEFL + [E*A*alpha*deltaT ; 0 ; 0 ; -E*A*alpha*deltaT ; 0 ; 0];

%This section takes into account any specified displacements

FEFL = FEFL + [specifiedDelta(1,1)*E*A/L ; 12*E*I*specifiedDelta(2,1)/L^3 ; 6*E*I*specifiedDelta(2,1)/L^2 ; -specifiedDelta(1,1)*E*A/L ; -12*E*I*specifiedDelta(2,1)/L^3 ; 6*E*I*specifiedDelta(2,1)/L^2]; %Adds the resulting forces due to temperature change to FEFL

%This section accounts for shrinkStrain
DeltaLShrink = L*shrinkStrain; %Calculates the total change in length due to shrinkstrain

FEFL = FEFL + [-DeltaLShrink*E*A/L ; 0 ; 0 ; DeltaLShrink*E*A/L ; 0 ;0]; %Computes forces from shrinkage and adds them to FEFL

output = FEFL;

end
% The above function takes load condition inputs along with the required section
% and material inputs. It computes the global FEF vector of an element


function [output] = GetStructureStiffnessMatrix(K,map)

CountNodes = size(K)+1;%Counts the number of nodes based on input. 
CountElements = size(K);%Counts the number of elements based on input. 
CountDoFs = CountNodes(1,2)*3;%Counts the number of DoFs, based on number of nodes

Ks = zeros(CountDoFs);%Creates a global structural matrix of zeros equal to the number of DoFs provided

for i = 1:CountElements(1,2)%Repeates the loop once for each element
KGlobalElem = zeros(CountDoFs);%Creates a second zeros matrix to temporarily store values
KGlobalElem(map{i},map{i}) = K{i};%Uses the zero matrix to create a global mapped stiffness matrix for each element
Ks = Ks + KGlobalElem;%Addes the global mapped stiffness matrix to the global structural stiffness matrix
end 

output = Ks;%Returns the global structure stiffness matrix

end
% The above function takes elements local stiffness matrix and adds
% them to form a structure stiffness matrix.