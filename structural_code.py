

import streamlit as st
import array as arr
import numpy as np
import math
from bokeh.plotting import figure, show

st.set_page_config(page_title='Structural Calculator', layout = 'centered', initial_sidebar_state = 'auto')

node_coordinates = list()
elements_Y = list()
elements_E = list()
elements_A = list()
elements_I = list()
elements_map = list()

st.sidebar.title("Instructions") #######Instruction to user in sidedar#############
st.sidebar.subheader("Element Definition")
st.sidebar.subheader("Coordinates are in meters.")
st.sidebar.write("Mapping vectors define how each element fits into the global DoF system.")
st.sidebar.write("Each digit should be seperated by commas.")

st.sidebar.subheader("Forces")
st.sidebar.write("All units are in Newtons")
st.sidebar.write("Force inputs are defined in the global coordinate system. y is upwards positive, x is right positive, and z is counterclockwise positive.")
st.sidebar.write("Enter zeros for any cells without inputs, do not leave blank.")
st.sidebar.write("Do not use scientific notation.")

st.sidebar.subheader("Support Vector")
st.sidebar.write("The support vector defines which DoFs are fixed and which are free. Enter 1 for fixed DoFs, and 0 for free DoFs.")
st.sidebar.write("DoFs are in the order of x1,y1,z1,x2,y2,z2, etc...")
 
st.title("Displacement and Reaction Force Calculator")

st.subheader("Element Properties and Definition")
try: #Number of elements input and confirm bounds of user input
    num_elements = st.text_input("Number of elements")
    num_elements = int(num_elements)
    
    if num_elements < 2:
        st.write("A minimum two elements are required for analysis")
        
        
    if num_elements > 5:
        st.write("Max number of elements is 5 at this time")
        num_elements = None
    

    W_Array = np.zeros((int(num_elements),3))
    Truss_Vector = np.zeros(int(num_elements))
except:
    print(" ")


try: #Element properties
    try:#Element 1 Properties 
        if int(num_elements) >= 2:

            col1,col2,col3,col4,col5,col6,col7,col8,col9 = st.columns([1,0.7,0.7,0.7,0.7,1,0.8,1,1.2])
            mapcol1,mapcol2 = st.columns([1,7])

            with col1:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write("Element 1")

            with col2:
                e1_x1 = col2_string = st.text_input("X1")
                
            with col3:
                e1_y1 = st.text_input("Y1")

            with col4:
                e1_x2 = st.text_input("X2")
                
            with col5:
                e1_y2 = st.text_input("Y2")

            with col6:
                e1_I = st.text_input("I (m^4)")
                
            with col7:
                e1_E = st.text_input("E (GPa)")

            with col8:
                e1_A = st.text_input("A (m^2)")
                
            with col9:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                checkbox1 = st.checkbox("Truss")
                if checkbox1:
                    Truss_Vector[0] = 1
                
            try:
                with mapcol1:
                    st.write(" ")
                    st.write(" ")
                    st.write("Mapping Vector")

                with mapcol2:
                    e1_map_raw = st.text_input(" ", value = "1,2,3,4,5,6")
                    e1_map_split = e1_map_raw.split(",")
                    e1_map_int = [int(i) for i in e1_map_split]
            except:
                print(" ")
                
            e1_both_coords = list()
            e1_coord1 = list()
            e1_coord1.append(e1_x1)
            e1_coord1.append(e1_y1)
            e1_coord1 = [float(i) for i in e1_coord1]
            e1_both_coords.append(e1_coord1)
       
            
            e1_coord2 = list()
            e1_coord2.append(e1_x2)
            e1_coord2.append(e1_y2)
            e1_coord2 = [float(i) for i in e1_coord2]
            e1_both_coords.append(e1_coord2)
            node_coordinates.append(e1_both_coords)
           
            elements_E.append(e1_E)
            elements_A.append(e1_A)
            elements_I.append(e1_I)
            elements_map.append(e1_map_int)
    except:
        st.write(" ")

    try:#Element 2 Properties
        if int(num_elements) >= 2:

            col11,col12,col13,col14,col15,col16,col17,col18,col19 = st.columns([1,0.7,0.7,0.7,0.7,1,0.8,1,1.2])
            mapcol19,mapcol20 = st.columns([1,7])

            with col11:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write("Element 2")

            with col12:
                e2_x1 = st.text_input("X1", key = 1)
                
            with col13:
                e2_y1 = st.text_input("Y1", key = 1)

            with col14:
                e2_x2 = st.text_input("X2", key = 1)
                
            with col15:
                e2_y2 = st.text_input("Y2", key = 1)

            with col16:
                e2_I = st.text_input("I (m^4)", key = 1)
                
            with col17:
                e2_E = st.text_input("E (GPa)", key = 1)

            with col18:
                e2_A = st.text_input("A (m^2)", key = 1)
                
            with col19:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                checkbox2 = st.checkbox("Truss",key = 1)
                if checkbox2:
                    Truss_Vector[1] = 1
            try:
            
                with mapcol19:
                    st.write(" ")
                    st.write(" ")
                    st.write("Mapping Vector")

                with mapcol20:
                    e2_map_raw = st.text_input(" ",key = 1,value="4,5,6,7,8,9")
                    e2_map_split = e2_map_raw.split(",")
                    e2_map_int = [int(i) for i in e2_map_split]
            except:
                print(" ") 
                
            e2_coord1 = list()
            e2_both_coords = list()
            e2_coord1.append(e2_x1)
            e2_coord1.append(e2_y1)
            e2_coord1 = [float(i) for i in e2_coord1]
            e2_both_coords.append(e2_coord1)
            
            e2_coord2 = list()
            e2_coord2.append(e2_x2)
            e2_coord2.append(e2_y2)
            e2_coord2 = [float(i) for i in e2_coord2]
            e2_both_coords.append(e2_coord2)
            node_coordinates.append(e2_both_coords)
           
            elements_E.append(e2_E)
            elements_A.append(e2_A)
            elements_I.append(e2_I)
            elements_map.append(e2_map_int)
    except:
        st.write(" ")
        
    try:#Element 3 Properties
        if int(num_elements) >= 3:

            col21,col22,col23,col24,col25,col26,col27,col28,col29 = st.columns([1,0.7,0.7,0.7,0.7,1,0.8,1,1.2])
            mapcol29,mapcol30 = st.columns([1,7])

            with col21:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write("Element 3")

            with col22:
                e3_x1 = st.text_input("X1", key = 2)
                
            with col23:
                e3_y1 = st.text_input("Y1", key = 2)

            with col24:
                e3_x2 = st.text_input("X2", key = 2)
                
            with col25:
                e3_y2 = st.text_input("Y2", key = 2)

            with col26:
                e3_I = st.text_input("I (m^4)", key = 2)
                
            with col27:
                e3_E = st.text_input("E (GPa)", key = 2)

            with col28:
                e3_A = st.text_input("A (m^2)", key = 2)
                
            with col29:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                checkbox3 = st.checkbox("Truss",key = 2)
                if checkbox3:
                    Truss_Vector[2] = 1
            try:
            
                with mapcol29:
                    st.write(" ")
                    st.write(" ")
                    st.write("Mapping Vector")

                with mapcol30:
                    e3_map_raw = st.text_input(" ",key = 2)
                    e3_map_split = e3_map_raw.split(",")
                    e3_map_int = [int(i) for i in e3_map_split]
            except:
                print(" ") 
                
            e3_coord1 = list()
            e3_both_coords = list()
            e3_coord1.append(e3_x1)
            e3_coord1.append(e3_y1)
            e3_coord1 = [float(i) for i in e3_coord1]
            e3_both_coords.append(e3_coord1)
            
            e3_coord2 = list()
            e3_coord2.append(e3_x2)
            e3_coord2.append(e3_y2)
            e3_coord2 = [float(i) for i in e3_coord2]
            e3_both_coords.append(e3_coord2)
            node_coordinates.append(e3_both_coords)
           
            elements_E.append(e3_E)
            elements_A.append(e3_A)
            elements_I.append(e3_I)
            elements_map.append(e3_map_int)
    except:
        st.write(" ")
        
    try:#Element 4 Properties
        if int(num_elements) >= 4:

            col31,col32,col33,col34,col35,col36,col37,col38,col39 = st.columns([1,0.7,0.7,0.7,0.7,1,0.8,1,1.2])
            mapcol39,mapcol40 = st.columns([1,7])

            with col31:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write("Element 4")

            with col32:
                e4_x1 = st.text_input("X1", key = 3)
                
            with col33:
                e4_y1 = st.text_input("Y1", key = 3)

            with col34:
                e4_x2 = st.text_input("X2", key = 3)
                
            with col35:
                e4_y2 = st.text_input("Y2", key = 3)

            with col36:
                e4_I = st.text_input("I (m^4)", key = 3)
                
            with col37:
                e4_E = st.text_input("E (GPa)", key = 3)

            with col38:
                e4_A = st.text_input("A (m^2)", key = 3)
                
            with col39:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                checkbox4 = st.checkbox("Truss",key = 3)
                if checkbox4:
                    Truss_Vector[3] = 1
            try:
            
                with mapcol39:
                    st.write(" ")
                    st.write(" ")
                    st.write("Mapping Vector")

                with mapcol40:
                    e4_map_raw = st.text_input(" ",key = 3)
                    e4_map_split = e4_map_raw.split(",")
                    e4_map_int = [int(i) for i in e4_map_split]
            except:
                print(" ") 
                
            e4_coord1 = list()
            e4_both_coords = list()
            e4_coord1.append(e4_x1)
            e4_coord1.append(e4_y1)
            e4_coord1 = [float(i) for i in e4_coord1]
            e4_both_coords.append(e4_coord1)
            
            e4_coord2 = list()
            e4_coord2.append(e4_x2)
            e4_coord2.append(e4_y2)
            e4_coord2 = [float(i) for i in e4_coord2]
            e4_both_coords.append(e4_coord2)
            node_coordinates.append(e4_both_coords)
           
            elements_E.append(e4_E)
            elements_A.append(e4_A)
            elements_I.append(e4_I)
            elements_map.append(e4_map_int)
    except:
        st.write(" ")
        
    try:#Element 5 Properties
        if int(num_elements) >= 5:

            col41,col42,col43,col44,col45,col46,col47,col48,col49 = st.columns([1,0.7,0.7,0.7,0.7,1,0.8,1,1.2])
            mapcol49,mapcol50 = st.columns([1,7])

            with col41:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write("Element 4")

            with col42:
                e5_x1 = st.text_input("X1", key = 4)
                
            with col43:
                e5_y1 = st.text_input("Y1", key = 4)

            with col44:
                e5_x2 = st.text_input("X2", key = 4)
                
            with col45:
                e5_y2 = st.text_input("Y2", key = 4)

            with col46:
                e5_I = st.text_input("I (m^4)", key = 4)
                
            with col47:
                e5_E = st.text_input("E (GPa)", key = 4)

            with col48:
                e5_A = st.text_input("A (m^2)", key = 4)
                
            with col49:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                checkbox5 = st.checkbox("Truss",key = 4)
                if checkbox5:
                    Truss_Vector[4] = 1
            try:
            
                with mapcol49:
                    st.write(" ")
                    st.write(" ")
                    st.write("Mapping Vector")

                with mapcol50:
                    e5_map_raw = st.text_input(" ",key = 4)
                    e5_map_split = e5_map_raw.split(",")
                    e5_map_int = [int(i) for i in e5_map_split]
            except:
                print(" ") 
                
            e5_coord1 = list()
            e5_both_coords = list()
            e5_coord1.append(e5_x1)
            e5_coord1.append(e5_y1)
            e5_coord1 = [float(i) for i in e5_coord1]
            e5_both_coords.append(e5_coord1)
            
            e5_coord2 = list()
            e5_coord2.append(e5_x2)
            e5_coord2.append(e5_y2)
            e5_coord2 = [float(i) for i in e5_coord2]
            e5_both_coords.append(e5_coord2)
            node_coordinates.append(e5_both_coords)
           
            elements_E.append(e5_E)
            elements_A.append(e5_A)
            elements_I.append(e5_I)
            elements_map.append(e5_map_int)
    except:
        st.write(" ")
        
except:
    st.write(" ")
                    
st.subheader("Forces")
num_pointloads = st.text_input("Number of Point Loads")

try: #Point Load Entry
    P_Array = np.zeros((int(num_elements),4)) #Creates a 2D array with number of vectors = number of elements, point loads are later mapped into this

    try:#Point Load 1
        if int(num_pointloads) >= 1:

            Fc1,Fc2,Fc3,Fc4,Fc5 = st.columns([0.6,1.1,1,1,1.1])
            
            with Fc1:
                F1_Node_ID = st.text_input("Element ID", key = 1)
                
            with Fc2:
                F1_Distance = st.text_input("Distance Along Element", key = 1)

            with Fc3:
                F1_Force_X = st.text_input("Force in X Direction", key = 1)
                
            with Fc4:
                F1_Force_Y = st.text_input("Force in Y Direction", key = 1)

            with Fc5:
                F1_Force_Z = st.text_input("Moment in Z Direction", key = 1)
                
            PL_1_vector = list()
            PL_1_vector.append(F1_Distance)
            PL_1_vector.append(F1_Force_X)
            PL_1_vector.append(F1_Force_Y)
            PL_1_vector.append(F1_Force_Z)
            PL_1_vector = [float(i) for i in PL_1_vector]
            
            P_Array[int(F1_Node_ID)-1] = P_Array[int(F1_Node_ID)-1] + PL_1_vector
    except:
        st.write(" ")
        
    try:#Point Load 2
        if int(num_pointloads) >= 2:
            Fc11,Fc12,Fc13,Fc14,Fc15 = st.columns([0.6,1.1,1,1,1.1])
            
            with Fc11:
                F2_Node_ID = st.text_input("Element ID", key = 2)
                
            with Fc12:
                F2_Distance = st.text_input("Distance Along Element", key = 2)

            with Fc13:
                F2_Force_X = st.text_input("Force in X Direction", key = 2)
                
            with Fc14:
                F2_Force_Y = st.text_input("Force in Y Direction", key = 2)

            with Fc15:
                F2_Force_Z = st.text_input("Moment in Z Direction", key = 2)
                
            if F2_Node_ID == F1_Node_ID:
                st.write("One element can not have two point loads, divide element in half to add additional point loads")
                
            PL_2_vector = list()
            PL_2_vector.append(F2_Distance)
            PL_2_vector.append(F2_Force_X)
            PL_2_vector.append(F2_Force_Y)
            PL_2_vector.append(F2_Force_Z)
            PL_2_vector = [float(i) for i in PL_2_vector]
            
            P_Array[int(F2_Node_ID)-1] = P_Array[int(F2_Node_ID)-1] + PL_2_vector
    except:
        st.write(" ")
        
    try:#Point Load 3
        if int(num_pointloads) >= 3:

            Fc21,Fc22,Fc23,Fc24,Fc25 = st.columns([0.6,1.1,1,1,1.1])
            
            with Fc21:
                F3_Node_ID = st.text_input("Element ID", key = 3)
                
            with Fc22:
                F3_Distance = st.text_input("Distance Along Element", key = 3)

            with Fc23:
                F3_Force_X = st.text_input("Force in X Direction", key = 3)
                
            with Fc24:
                F3_Force_Y = st.text_input("Force in Y Direction", key = 3)

            with Fc25:
                F3_Force_Z = st.text_input("Moment in Z Direction", key = 3)
                
            if F3_Node_ID == F2_Node_ID or F3_Node_ID == F2_Node_ID:
                st.write("One element can not have two point loads, divide element in half to add additional point loads")
                
            PL_3_vector = list()
            PL_3_vector.append(F3_Distance)
            PL_3_vector.append(F3_Force_X)
            PL_3_vector.append(F3_Force_Y)
            PL_3_vector.append(F3_Force_Z)
            PL_3_vector = [float(i) for i in PL_3_vector]
            
            P_Array[int(F3_Node_ID)-1] = P_Array[int(F3_Node_ID)-1] + PL_3_vector
    except:
        st.write(" ")
        
    try:#Point Load 4
        if int(num_pointloads) >= 4:

            Fc31,Fc32,Fc33,Fc34,Fc35 = st.columns([0.6,1.1,1,1,1.1])
            
            with Fc31:
                F4_Node_ID = st.text_input("Element ID", key = 4)
                
            with Fc32:
                F4_Distance = st.text_input("Distance Along Element", key = 4)

            with Fc33:
                F4_Force_X = st.text_input("Force in X Direction", key = 4)
                
            with Fc34:
                F4_Force_Y = st.text_input("Force in Y Direction", key = 4)

            with Fc35:
                F4_Force_Z = st.text_input("Moment in Z Direction", key = 4)
                
            if F4_Node_ID == F3_Node_ID or F4_Node_ID == F2_Node_ID or F4_Node_ID == F1_Node_ID:
                st.write("One element can not have two point loads, divide element in half to add additional point loads")
                
            PL_4_vector = list()
            PL_4_vector.append(F4_Distance)
            PL_4_vector.append(F4_Force_X)
            PL_4_vector.append(F4_Force_Y)
            PL_4_vector.append(F4_Force_Z)
            PL_4_vector = [float(i) for i in PL_4_vector]
            
            P_Array[int(F4_Node_ID)-1] = P_Array[int(F4_Node_ID)-1] + PL_4_vector
    except:
        st.write(" ")
        
    try:#Point Load 5
        if int(num_pointloads) >= 5:

            Fc41,Fc42,Fc43,Fc44,Fc45 = st.columns([0.6,1.1,1,1,1.1])
            
            with Fc41:
                F5_Node_ID = st.text_input("Element ID", key = 5)
                
            with Fc42:
                F5_Distance = st.text_input("Distance Along Element", key = 5)

            with Fc43:
                F5_Force_X = st.text_input("Force in X Direction", key = 5)
                
            with Fc44:
                F5_Force_Y = st.text_input("Force in Y Direction", key = 5)

            with Fc45:
                F5_Force_Z = st.text_input("Moment in Z Direction", key = 5)
                
            if F5_Node_ID == F4_Node_ID or F5_Node_ID == F3_Node_ID or F5_Node_ID == F2_Node_ID or F5_Node_ID == F1_Node_ID:
                st.write("One element can not have two point loads, divide element in half to add additional point loads")
                
            PL_5_vector = list()
            PL_5_vector.append(F5_Distance)
            PL_5_vector.append(F5_Force_X)
            PL_5_vector.append(F5_Force_Y)
            PL_5_vector.append(F5_Force_Z)
            PL_5_vector = [float(i) for i in PL_5_vector]
            
            P_Array[int(F5_Node_ID)-1] = P_Array[int(F5_Node_ID)-1] + PL_5_vector 
    except:
        st.write(" ")
    
except:
    st.write(" ")
        
num_dist_loads = st.text_input("Number of Distributed Loads")
    
try:#Distributed load entry
    try:#Dist Load 1
        if int(num_dist_loads) >= 1:

            Dc1,Dc2,Dc3,Dc4 = st.columns([0.6,1.1,1,1,])
            
            with Dc1:
                D1_Ele_ID = st.text_input("Element ID", key = 3)
                
            with Dc2:
                Dc2_X = st.text_input("In X Direction", key = 3)

            with Dc3:
                Dc3_Y = st.text_input("in Y Direction", key = 3)
                
            with Dc4:
                Dc4_Z = st.text_input("In Z Direction", key = 3)



            W_1_vector = list()
            W_1_vector.append(Dc2_X)
            W_1_vector.append(Dc3_Y)
            W_1_vector.append(Dc4_Z)
            W_1_vector = [float(i) for i in W_1_vector]
            
            W_Array[int(D1_Ele_ID)-1] = W_Array[int(D1_Ele_ID)-1] + W_1_vector #Maps the inputted distributed vector into the correct W_Array location
    except:
        st.write(" ")
        
    try:#Dist Load 2
        if int(num_dist_loads) >= 2:

            Dc11,Dc12,Dc13,Dc14 = st.columns([0.6,1.1,1,1,])
            
            with Dc11:
                D2_Ele_ID = st.text_input("Element ID", key = 4)
                
            with Dc12:
                Dc12_X = st.text_input("In X Direction", key = 4)

            with Dc13:
                Dc13_Y = st.text_input("in Y Direction", key = 4)
                
            with Dc14:
                Dc14_Z = st.text_input("In Z Direction", key = 4)

         
            W_2_vector = list()
            W_2_vector.append(Dc12_X)
            W_2_vector.append(Dc13_Y)
            W_2_vector.append(Dc14_Z)
            W_2_vector = [float(i) for i in W_2_vector]
            
            W_Array[int(D2_Ele_ID)-1] = W_Array[int(D2_Ele_ID)-1] + W_2_vector
    except:
        st.write(" ")
        
    try:#Dist Load 3
        if int(num_dist_loads) >= 3:

            Dc21,Dc22,Dc23,Dc24 = st.columns([0.6,1.1,1,1,])
            
            with Dc21:
                D3_Ele_ID = st.text_input("Element ID", key = 5)
                
            with Dc22:
                Dc22_X = st.text_input("In X Direction", key = 5)

            with Dc23:
                Dc23_Y = st.text_input("in Y Direction", key = 5)
                
            with Dc24:
                Dc24_Z = st.text_input("In Z Direction", key = 5)

         
            w_3_vector = list()
            w_3_vector.append(Dc22_X)
            w_3_vector.append(Dc23_Y)
            w_3_vector.append(Dc24_Z)
            w_3_vector = [float(i) for i in w_3_vector]
            
            W_Array[int(D3_Ele_ID)-1] = W_Array[int(D3_Ele_ID)-1] + w_3_vector
    except:
        st.write(" ")
        
    try:#Dist Load 4
        if int(num_dist_loads) >= 4:

            Dc31,Dc32,Dc33,Dc34 = st.columns([0.6,1.1,1,1,])
            
            with Dc31:
                D4_Ele_ID = st.text_input("Element ID", key = 6)
                
            with Dc32:
                Dc32_X = st.text_input("In X Direction", key = 6)

            with Dc33:
                Dc33_Y = st.text_input("in Y Direction", key = 6)
                
            with Dc34:
                Dc34_Z = st.text_input("In Z Direction", key = 6)

         
            w_4_vector = list()
            w_4_vector.append(Dc32_X)
            w_4_vector.append(Dc33_Y)
            w_4_vector.append(Dc34_Z)
            w_4_vector = [float(i) for i in w_4_vector]
            
            W_Array[int(D4_Ele_ID)-1] = W_Array[int(D4_Ele_ID)-1] + w_4_vector
    except:
        st.write(" ")
        
    try:#Dist Load 5
        if int(num_dist_loads) >= 5:

            Dc41,Dc42,Dc43,Dc44 = st.columns([0.6,1.1,1,1,])
            
            with Dc41:
                D5_Ele_ID = st.text_input("Element ID", key = 7)
                
            with Dc42:
                Dc42_X = st.text_input("In X Direction", key = 7)

            with Dc43:
                Dc43_Y = st.text_input("in Y Direction", key = 7)
                
            with Dc44:
                Dc44_Z = st.text_input("In Z Direction", key = 7)

         
            w_5_vector = list()
            w_5_vector.append(Dc42_X)
            w_5_vector.append(Dc43_Y)
            w_5_vector.append(Dc44_Z)
            w_5_vector = [float(i) for i in w_5_vector]
            
            W_Array[int(D5_Ele_ID)-1] = W_Array[int(D5_Ele_ID)-1] + w_5_vector
    except:
        st.write(" ")
        
except:
    st.write(" ")

st.subheader("Supports")

Coordinates_Array = np.array(node_coordinates)
num_nodes = len(Coordinates_Array)+1 #Computes number of nodes based on user input
num_DoFs = num_nodes*3 #Computes number of DoFs

#This section creates the placeholder for the support vector user entry #######################################
supp_string_placehold = ""
string_of_zeros = list() 

if num_DoFs > 8: #Only generates placeholder when more than 9 DoFs
    for i in range(num_DoFs): #This loop adds zeros and commas to list
        string_of_zeros.append("0")
        if i < num_DoFs-1: #If statement needed to not add a last comma
            string_of_zeros.append(",")
    supp_string_placehold = np.array(string_of_zeros) #Converts placeholder of support vector into an array

supp_string = st.text_input("Support Vector",value = ''.join(supp_string_placehold)) #Joins the string values within the array into a string

try: #Defines arrays 
    supp_string_split= supp_string.split(",")
    supp_string_int = [int(i) for i in supp_string_split]


    #User input ends # All code below is calculations

    elements_A = [float(i) for i in elements_A]
    elements_E = [float(i) for i in elements_E]
    elements_I = [float(i) for i in elements_I]



    E_Array = np.array(elements_E)*1000*1000*1000 #Converts to GPa
    A_Array = np.array(elements_A)
    I_Array = np.array(elements_I)
    map_Array = np.array(elements_map)
    supp_Array = np.array(supp_string_int)
except:
    st.write(" ")
     
x_coords = list()    
y_coords = list()

try:#####################This section plots the elements############################################ IN PROGRESS
    for i in range(len(Coordinates_Array)):
        for j in range(2):
            x_coords.append(Coordinates_Array[i][j][0]) #Appends all x coordinates into a single list
            y_coords.append(Coordinates_Array[i][j][1]) #Appends all y coordinates into a single list
        x_coords.append("Nan") #Inserts "NaN" between each node so that each element is plotted individually
        y_coords.append("Nan") #Inserts "NaN" between each node so that each element is plotted individually
           
    p = figure(x_axis_label='x',y_axis_label='y', match_aspect=True)
    p.line(x_coords, y_coords, line_width=4)
    st.bokeh_chart(p, use_container_width=True)
    
    x_coords_div = list()
    x_coords_partitioned = list()
    y_coords_div = list()
    y_coords_partitioned = list()
    test = list()

    for i in range(0,num_elements*2,2): #This code is currently not used
        x_coords_div_array = np.zeros((2))
        x_coords_div.clear()
        x_coords_div.append(x_coords[i])
        x_coords_div.append(x_coords[i+1])
        x_coords_div_array[0] = x_coords_div[0]
        x_coords_div_array[1] = x_coords_div[1]
        x_coords_partitioned.append(x_coords_div_array)
        
        y_coords_div_array = np.zeros((2))
        y_coords_div.clear()
        y_coords_div.append(y_coords[i])
        y_coords_div.append(y_coords[i+1])
        y_coords_div_array[0] = y_coords_div[0]
        y_coords_div_array[1] = y_coords_div[1]
        y_coords_partitioned.append(y_coords_div_array)
    
except:
    st.write(" ")


#p = figure(x_axis_label='x',y_axis_label='y', match_aspect=True)
#p.multi_line(testx, testy, line_width=4)
#st.bokeh_chart(p, use_container_width=True)


def GetGlobalTransformationMatrix(nodei,nodej,Truss):

    

    #nodei = int(np.array(nodei))
    #nodej = int(np.array(nodej))

    #DeltaX = np.zero(2)
    #DeltaY = np.array(2)
    
    DeltaX = nodej[0] - nodei[0] #Creates two variables 'DeltaX' and 'DeltaY'to calculate the global horizontal displacement and global vertical displacement respectively
    DeltaY = nodej[1] - nodei[1]
    
    T = np.zeros((6,6))

    #The following 6 if statements account for any cases of nodei and nodej arrangements

    if DeltaX > 0 and DeltaY >= 0: #For positive DeltaX and DeltaY (or DeltaY==0) (1st quadrant)
        Theta = 2*math.pi - math.atan(DeltaY/DeltaX)
    

    if DeltaX < 0 and DeltaY >= 0: #For Negative DetlaX and Positive DeltaY (or DeltaY==0) (2nd quadrant)
        Theta = math.pi + math.atan(DeltaY/abs(DeltaX))


    if DeltaX < 0 and DeltaY < 0: #For Negative DeltaX and DeltaY (3rd Quadrant)
        Theta = math.pi - math.atan(abs(DeltaY)/abs(DeltaX))


    if DeltaX > 0 and DeltaY < 0: #For Positive DeltaX and Negative DeltaY (4th quadrant)
        Theta = math.atan(abs(DeltaY)/DeltaX)


    if DeltaX == 0 and DeltaY > 0: #For when DeltaX == 0 and DeltaY > 0 (Element vertical and upwards)
        Theta = 3/2*math.pi


    if DeltaX == 0 and DeltaY < 0: #For when Delta == 0 and DeltaY < 0 (Elemtent vertical and downwards)
        Theta = 1/2*math.pi


    if Truss == 1: #Truss == 1 is for truss members
        T = ([math.cos(Theta),math.sin(Theta),0,0,0,0],[-math.sin(Theta),math.cos(Theta),0,0,0,0],[0,0,0,0,0,0],[0,0,0,math.cos(Theta),math.sin(Theta),0],[0,0,0,-math.sin(Theta),math.cos(Theta),0],[0,0,0,0,0,0])

    if Truss == 0: #Uses the angle 'Theta' (measured positive and CCW) to produce the coordinate transformation matrix of the given element
        T = ([math.cos(Theta),math.sin(Theta),0,0,0,0],[-math.sin(Theta),math.cos(Theta),0,0,0,0],[0,0,1,0,0,0],[0,0,0,math.cos(Theta),math.sin(Theta),0],[0,0,0,-math.sin(Theta),math.cos(Theta),0],[0,0,0,0,0,1])
    return T
        
def GetLocalStiffnessMatrix(nodei,nodej,E,I,A,Truss):

    # Computes the horizontal and vertical component of the element and stores them in the variables deltaX and deltaY respectively
    deltaX = nodej[0] - nodei[0]
    deltaY = nodej[1] - nodei[1]

    # Uses deltaX and deltaY to compute the elements length
    L = math.sqrt(deltaX**2 + deltaY**2)

    # For simplicity, each term within the stiffness matrix is calculated and 
    # stored within a seperate variable (a,b,c, and d)

    a = E*A/L
    b = 12*E*I/L**3
    c = 6*E*I/L**2
    d = 4*E*I/L

    Klocal = ([a,0,0,-a,0,0],[0,b,c,0,-b,c],[0,c,d,0,-c,d/2],[-a,0,0,a,0,0],[0,-b,-c,0,b,-c],[0,c,d/2,0,-c,d])# Formulates the local stiffness matrix as derived in problem 1 of HW2.

    if Truss == 1:
        Klocal = ([a,0,0,-a,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[-a,0,0,a,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0])
        
    return Klocal# Outputs the local stiffness matrix of the given element

def GetLocalFEFs(nodei,nodej,E,I,A,P,w):

    FEFL = np.zeros((6,1))

    DeltaX = nodej[0] - nodei[0] #Computes DeltaX between nodei and nodej
    DeltaY = nodej[1] - nodei[1] #Computes DeltaY between nodei and nodej
   

    L = math.sqrt(DeltaX**2+DeltaY**2) #Computes the length of the element using DeltaX and DeltaY

    #This section of code creates a 6x1 vector representing local fixed end forces. It accounts for any applied loads in 
    #the X and Y directions and adds the resulting FEFs to the vector.
    Py = P[2]
    Px = P[1]
    a = P[0]
    b = L-a

    FEFL = FEFL + ([-Px*b/L ],[ -Py*b**2*(3*a+b)/L**3 ],[ -Py*b**2*a/L**2 ],[ -Px*a/L ],[ -Py*a**2*(b*3+a)/L**3 ],[ Py*b*a**2/L**2])

    #This section accounts for any applied moments in the z direction and addes them to the FEFL
    M = P[3]
 
    FEFL = FEFL + ([0],[ 6*M*a*b/L**3 ],[ M*b*(2*a-b)/L**2 ],[ 0 ],[ -6*M*a*b/L**3 ],[ M*a*(2*b-a)/L**2 ])

    #This section calculates FEFs from any distributed loads in the x,y, or z direction and adds them to FEFL
    Wx = w[0]
    Wy = w[1]
    Wz = w[2]

    FEFL = FEFL + ([-Wx*L/2 ],[ -Wy*L/2 + Wz ],[ -Wy*L**2/12 ],[ -Wx*L/2 ],[ -Wy*L/2 - Wz],[ Wy*L**2/12])

    return FEFL

def GetStructureStiffnessMatrix(K,map_Array): 

    CountNodes = len(K)+1 #Counts the number of nodes based on input. 
    CountElements = len(K) #Counts the number of elements based on input. 
    CountDoFs = CountNodes*3 #Counts the number of DoFs, based on number of nodes

    Ks = np.zeros((CountDoFs,CountDoFs)) #Creates a global structural matrix of zeros equal to the number of DoFs provided

    for i in range(0,CountElements): #Repeates the loop once for each element
    
        KGlobalElem = np.zeros((CountDoFs,CountDoFs)) #Creates a second zeros matrix to temporarily store values
        
        KGlobalElem[np.ix_(map_Array[i]-1,map_Array[i]-1)] = K[i] #Uses the zero matrix to create a global mapped stiffness matrix for each element
        
        Ks = Ks + KGlobalElem #Addes the global mapped stiffness matrix to the global structural stiffness matrix

    return Ks;#Returns the global structure stiffness matrix

try: #Main calc try loop

    if sum(supp_Array) > 0: #Only runs calcualtions if at least one DoF is defined as fixed
        #The below lines pre-specify three dimensional 6x6 arrays equal to number of elements
        T = np.zeros((num_elements,6,6))
        KLocal = np.zeros((num_elements,6,6))
        KGlobal = np.zeros((num_elements,6,6))
        FEFLocal = np.zeros((num_elements,6))
        FEFGlobal = np.zeros((num_elements,6))


        Global_Force_Vector = np.zeros((num_DoFs)) #Creates a global force vector, each elements global force vectors will be mapped into this

        for i in range(0,num_elements): #This loop computes K GLobal and Global Force Vector for all elements

            T[i] = np.array(GetGlobalTransformationMatrix(Coordinates_Array[i][0],Coordinates_Array[i][1],Truss_Vector[i]))
            KLocal[i] = GetLocalStiffnessMatrix(Coordinates_Array[i,0],Coordinates_Array[i,1],E_Array[i],I_Array[i],A_Array[i],Truss_Vector[i])
            KGlobal[i] = np.matmul(np.matmul(T[i],KLocal[i]),np.transpose(T[i]))
            FEFLocal[i] = np.transpose(GetLocalFEFs(Coordinates_Array[i,0],Coordinates_Array[i,1],E_Array[i],I_Array[i],A_Array[i],P_Array[i],W_Array[i])) #Uses function to get fixed end forces in local coordinates and stores them in an array
            #FEFGlobal[i] = np.matmul(T[i],FEFLocal[i]) ###########Uncomment this and add to FEF_Element_Mapped to change from global force input to local force input
            
            FEF_Element_Mapped = np.zeros((num_DoFs)) #Creates a new zeros vector to temporaily store Global forces in
            FEF_Element_Mapped[map_Array[i]-1] = FEFLocal[i] #Maps the elements global force vectors into a mapped vector, -1 because array index starts at 0
            
            Global_Force_Vector = Global_Force_Vector + FEF_Element_Mapped

        KStructure = GetStructureStiffnessMatrix(KGlobal,map_Array)

        #The below code relates to the partitioning of the KStructure

        support_Locations = np.zeros(num_DoFs,dtype=int)
        free_Locations = np.zeros(num_DoFs,dtype = int)

        for i in range(0,num_DoFs,1): #Repeats loop once for each DoF
            
            if supp_Array[i] == 1: #The empty vector defined above gets assigned support locations based on user input. IE: supportLocations = [[0,2,0,0,5], in this system the user defined node 2 and 5 as fixed.
                support_Locations[i] = i+1 #i+1 because indexing starts at 0, non zero function will delete the first entry which it shouldnt
            
            if supp_Array[i] == 0: #Same as above, the empty vector defined above gets assigned free locations based on user input.
                free_Locations[i] = i+1

        support_Locations = np.nonzero(support_Locations)
        free_Locations = np.nonzero(free_Locations)

        num_supports = np.sum(supp_Array) #Counts the number of fixed DoFs in the system
        num_free = num_DoFs - num_supports #Counts the number of free DoFs in the system

        Kss = np.zeros((num_supports,num_supports))
        Ksf = np.zeros((num_supports,num_free))
        Kff = np.zeros((num_free,num_free))
        Kfs = np.zeros((num_free,num_supports))


        support_Locations = np.array(support_Locations) #The nonzero function put support_Locations and free_Locations into a wierd format so this converts it back
        free_Locations = np.array(free_Locations)

        support_Locations = support_Locations.flatten() #Flatten the support_Locations and free_Locations because they were being recognized as 2d instead of 1d
        free_Locations = free_Locations.flatten()


        Kss = KStructure[np.ix_(support_Locations,support_Locations)] #Assigns the fixed rows and fixed columns of KStructure to Kss
        Ksf = KStructure[np.ix_(support_Locations,free_Locations)] #Assigns the fixed rows and free columns of KStrucutre to Ksf
        Kff = KStructure[np.ix_(free_Locations,free_Locations)] #Assigns the free rows and free columns of KStrucutre to Kff
        Kfs = KStructure[np.ix_(free_Locations,support_Locations)] #Assigns the free rows and fixed columns of KStrucutre to Kss

        FEFS = np.zeros(num_supports)
        FEFf = np.zeros(num_free)

        FEFs = (Global_Force_Vector[support_Locations]) #Defines a vector containing only FEFs at supports that arise from load conditions 
        FEFf = (Global_Force_Vector[free_Locations]) #Defines a vector that contains only FEFs at free DoFs that arise from load conditions

        deltaf = np.zeros(num_free)
        Rs = np.zeros(num_supports)

        deltaf = np.matmul(np.linalg.inv(Kff),FEFf)*-1 #finds displacements at free DOFs, units are meters
        Rs = np.matmul(Ksf,deltaf)+FEFs #finds reactions at fixed DOFs, units are N

        deltaf_mapped = np.zeros(num_DoFs) #Creates a zeros vector of equal size to the number of DoFs
        deltaf_mapped[free_Locations] = deltaf #Returns displacements of every node in the order the nodes were inputted 

        Rs_mapped = np.zeros(num_DoFs); #Creates a zeros vector of equal size to the number of DoFs
        Rs_mapped[support_Locations] = Rs; #Returns reaction forces of every node in the order the nodes were inputted
        

        #Back end calculations finished, below code is output to streamlit
        

        col_filler1,col_displacement, col_reactioin,col_filler2 = st.columns([0.3,1,1,0.3])

        Max_DoFs_String = np.array(["x1","y1","z1","x2","y2","z2","x3","y3","z3","x4","y4","z4","x5","y5","z6","x6","y6","z6"])
        DoFs_to_Display = np.zeros(num_DoFs,dtype=object)
        Rs_with_DoFs = np.zeros((num_DoFs,2),dtype=object)
        deltaf_with_DoFs = np.zeros((num_DoFs,2),dtype=object)

        for i in range(num_DoFs):
            DoFs_to_Display[i] = Max_DoFs_String[i]
            
        with col_filler1:
            st.write(" ")

        with col_displacement:
            st.subheader("Displacements")
            units_disp = st.radio("Units to display",("μm","mm","m"))
            if units_disp == "μm":
                deltaf_mapped = deltaf_mapped*1000*1000
            if units_disp == "mm":
                deltaf_mapped = deltaf_mapped*1000
            if units_disp == "m":
                deltaf_mapped = deltaf_mapped
            deltaf_with_DoFs[0:num_DoFs,0] = DoFs_to_Display
            deltaf_with_DoFs[0:num_DoFs,1] = deltaf_mapped
            st.table(deltaf_with_DoFs)

                
        with col_reactioin:
            st.subheader("Reaction Forces")
            units_force = st.radio("Units to display",("N","kN","MN"))
            if units_force == "N":
                Rs_mapped = Rs_mapped
            if units_force == "kN":
                Rs_mapped = Rs_mapped/1000
            if units_force == "MN":
                Rs_mapped = Rs_mapped/1000/1000
                
            Rs_with_DoFs[0:num_DoFs,0] = DoFs_to_Display
            Rs_with_DoFs[0:num_DoFs,1] = Rs_mapped
            st.table(Rs_with_DoFs)
            
        with col_filler2:
            st.write(" ")
        show_calcs = st.button("Show Intermediate Calculations")
except:
    st.write(" ")
    

try: #Show Calcs try loop 
    if show_calcs:

        st.subheader("Local to Global Transformation Matrices") #Transformation matrix output below##############
        
        colT1,colT1_data = st.columns([1,8])
        colT2,colT2_data = st.columns([1,8])
        colT3,colT3_data = st.columns([1,8])
        colT4,colT4_data = st.columns([1,8])
        colT5,colT5_data = st.columns([1,8])
        
        with colT1:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.subheader("T1")
        with colT1_data:
            st.write(T[0])
            
        with colT2:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.subheader("T2")
        with colT2_data:
            st.write(T[1])
            
        if num_elements >= 3:
            with colT3:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("T3")
            with colT3_data:
                st.write(T[2])
                
        if num_elements >= 4:
            with colT4:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("T4")
            with colT4_data:
                st.write(T[3])
                
        if num_elements >= 5:
            with colT5:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("T5")
            with colT5_data:
                st.write(T[4])
                
        st.subheader("Local Stiffness Matrices") #Local stiffness matrices output below#######################
        
        colKl1,colKl1_data = st.columns([1.5,7])
        colKl2,colKl2_data = st.columns([1.5,7])
        colKl3,colKl3_data = st.columns([1.5,7])
        colKl4,colKl4_data = st.columns([1.5,7])
        colKl5,colKl5_data = st.columns([1.5,7])
        
        KLocal = KLocal.astype(int) #Converts KLocal to integer so streamlit doesnt show decimals
        
        with colKl1:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.subheader("KLocal 1")
        with colKl1_data:
            st.table(np.around(KLocal[0]))
        
        with colKl2:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.subheader("KLocal 2")
        with colKl2_data:
            st.table(np.around(KLocal[1]))
            
        if num_elements >= 3:
            with colKl3:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("KLocal 3")
            with colKl3_data:
                st.table(np.around(KLocal[2]))
                
        if num_elements >= 4:
            with colKl4:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("KLocal 4")
            with colKl4_data:
                st.table(np.around(KLocal[3]))
                
        if num_elements >= 5:
            with colKl5:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("KLocal 5")
            with colKl5_data:
                st.table(np.around(KLocal[4]))
                
        st.subheader("Global Stiffness Matrices") #Global Stiffness matrices below#######################
        
        colKg1,colKg1_data = st.columns([1.5,7])
        colKg2,colKg2_data = st.columns([1.5,7])
        colKg3,colKg3_data = st.columns([1.5,7])
        colKg4,colKg4_data = st.columns([1.5,7])
        colKg5,colKg5_data = st.columns([1.5,7])
        
        KGlobal = KGlobal.astype(int)
        
        with colKg1:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.subheader("KGlocal 1")
        with colKg1_data:
            st.table(np.around(KGlobal[0]))
        
        with colKg2:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.subheader("KGlobal 2")
        with colKg2_data:
            st.table(np.around(KGlobal[1]))
            
        if num_elements >= 3:
            with colKg3:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("KGlobal 3")
            with colKg3_data:
                st.table(np.around(KGlobal[2]))
                
        if num_elements >= 4:
            with colKg4:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("KGlobal 4")
            with colKg4_data:
                st.table(np.around(KGlobal[3]))
                
        if num_elements >= 5:
            with colKg5:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.subheader("KGlobal 5")
            with colKg5_data:
                st.table(np.around(KGlobal[4]))
                
        st.subheader("KStructure")
        KStructure = KStructure.astype(int)
        st.write(KStructure)
        
        
        
        st.subheader("Kss")
        Kss = Kss.astype(int)
        st.write(Kss)
        
        st.subheader("Ksf")
        Ksf = Ksf.astype(int)
        st.write(Ksf)
        
        st.subheader("Kff")
        Kff = Kff.astype(int)
        st.write(Kff)
        
        st.subheader("Kfs")
        Kfs = Kfs.astype(int)
        st.write(Kfs)
except:
    st.write(" ")
