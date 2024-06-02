import streamlit as st
import pandas as pd
import random
import datetime

## SQL DATABASE CODE
import sqlite3


conn = sqlite3.connect("drug_data.db",check_same_thread=False)
c = conn.cursor()

def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table create Successfully')

def customer_add_data(Cname,Cpass, Cemail, Cstate,Cnumber):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_State, C_Number) VALUES(?,?,?,?,?)''', (Cname,Cpass,  Cemail, Cstate,Cnumber))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data
def customer_update(Cemail,Cnumber):
    c.execute(''' UPDATE Customers SET C_Number = ? WHERE C_Email = ?''', (Cnumber,Cemail,))
    conn.commit()
    print("Updating")
def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
    conn.commit()

def drug_update(Duse, Did):
    c.execute(''' UPDATE Drugs SET D_Use = ? WHERE D_id = ?''', (Duse,Did))
    conn.commit()
def drug_delete(Did):
    c.execute(''' DELETE FROM Drugs WHERE D_id = ?''', (Did,))
    conn.commit()

def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL, 
                D_id INT PRIMARY KEY NOT NULL,
                Supplier_ID VARCHAR(50),
                FOREIGN KEY (Supplier_ID) REFERENCES Suppliers(S_ID))
                ''')
    print('DRUG Table create Successfully')

def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did, Supplier_ID):
    c.execute('''INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_id, Supplier_ID) VALUES(?,?,?,?,?,?)''', (Dname, Dexpdate, Duse, Dqty, Did, Supplier_ID))
    conn.commit()

def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data

def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL,
                C_Email VARCHAR(50),
                FOREIGN KEY (C_Email) REFERENCES Customers(C_Email))
    ''')

def order_delete(Oid):
    c.execute(''' DELETE FROM Orders WHERE O_id = ?''', (Oid,))
    conn.commit()

def order_add_data(O_Name,O_Items,O_Qty,O_id):
    c.execute('''INSERT INTO Orders (O_Name, O_Items,O_Qty, O_id) VALUES(?,?,?,?)''',
              (O_Name,O_Items,O_Qty,O_id))
    conn.commit()


def order_view_data(customername):
    c.execute('SELECT * FROM ORDERS Where O_Name == ?',(customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM ORDERS')
    order_all_data = c.fetchall()
    return order_all_data

def create_suppliers_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Suppliers(
                S_ID VARCHAR(50) PRIMARY KEY NOT NULL,
                S_Name VARCHAR(50) NOT NULL,
                S_Contact VARCHAR(50) NOT NULL,
                Drugs_Supplied VARCHAR(100) NOT NULL
                )''')
    conn.commit()
    print('Suppliers Table Created Successfully')

def add_supplier(s_id, s_name, s_contact, drugs_supplied):
    c.execute('''INSERT INTO Suppliers (S_ID, S_Name, S_Contact, Drugs_Supplied) VALUES (?, ?, ?, ?)''', (s_id, s_name, s_contact, drugs_supplied))
    conn.commit()

def view_all_suppliers():
    c.execute('SELECT * FROM Suppliers')
    return c.fetchall()

def delete_supplier(s_id):
    c.execute('''DELETE FROM Suppliers WHERE S_ID = ?''', (s_id,))
    conn.commit()

def create_transactions_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Transactions(
                Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                D_id INT NOT NULL,
                C_Email VARCHAR(50) NOT NULL,
                Quantity_Sold INT NOT NULL,
                Total_Price DECIMAL NOT NULL,
                Transaction_Date DATETIME NOT NULL,
                FOREIGN KEY (D_id) REFERENCES Drugs(D_id),
                FOREIGN KEY (C_Email) REFERENCES Customers(C_Email)
                )''')
    conn.commit()
    print('Transactions Table Created Successfully')

def add_transaction(D_id, C_Email, Quantity_Sold, Total_Price):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO Transactions (D_id, C_Email, Quantity_Sold, Total_Price, Transaction_Date) VALUES (?, ?, ?, ?, ?)''', (D_id, C_Email, Quantity_Sold, Total_Price, current_date))
    conn.commit()
    reduce_drug_quantity(D_id, Quantity_Sold)

def reduce_drug_quantity(D_id, Quantity_Sold):
    c.execute('UPDATE Drugs SET D_Qty = D_Qty - ? WHERE D_id = ?', (Quantity_Sold, D_id))
    conn.commit()

def view_all_transactions():
    c.execute('SELECT * FROM Transactions')
    return c.fetchall()

def admin():


    st.title("Pharmacy Database Dashboard")
    menu = ["Drugs", "Customers", "Orders", "Suppliers", "Transactions", "About"]
    choice = st.sidebar.selectbox("Menu", menu)



    ## DRUGS
    if choice == "Drugs":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_area("When to Use")
            with col2:
                drug_quantity = st.text_area("Enter the quantity")
                drug_id = st.text_area("Enter the Drug id (example:#D1)")
                supplier_id = st.selectbox("Select Supplier ID", [s_id[0] for s_id in view_all_suppliers()])

            if st.button("Add Drug"):
                drug_add_data(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_id, supplier_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            #st.write(drug_result)
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(drug_clean_df)
            with st.expander("View Drug Quantity"):
                drug_name_quantity_df = drug_clean_df[['Name','Quantity']]
                #drug_name_quantity_df = drug_name_quantity_df.reset_index()
                st.dataframe(drug_name_quantity_df)
        if choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_area("Drug ID")
            d_use = st.text_area("Drug Use")
            if st.button(label='Update'):
                drug_update(d_use,d_id)

        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_area("Drug ID")
            if st.button(label="Delete"):
                drug_delete(did)



    ## CUSTOMERS
    elif choice == "Customers":

        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password","Email-ID" ,"Area", "Number"])
                st.dataframe(cust_clean_df)

        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email,cust_number)

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)

    elif choice == "Orders":

        menu = ["View", "Delete"]  # Add "Delete" option
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID"])
                st.dataframe(order_clean_df)
        if choice == "Delete":
            st.subheader("Delete Order")
            O_id = st.text_input("Order ID")
            if st.button("Delete Order"):
                order_delete(O_id)
                st.success(f"Order {O_id} deleted successfully")
    elif choice == "Suppliers":
        supplier_menu = ["Add", "View", "Delete"]
        supplier_choice = st.sidebar.selectbox("Supplier Menu", supplier_menu)
        if supplier_choice == "Add":
            st.subheader("Add New Supplier")
            s_id = st.text_input("Supplier ID")
            s_name = st.text_input("Supplier Name")
            s_contact = st.text_input("Contact Details")
            drugs_supplied = st.text_area("Drugs Supplied")
            if st.button("Add Supplier"):
                add_supplier(s_id, s_name, s_contact, drugs_supplied)
                st.success("Supplier added successfully")
        elif supplier_choice == "View":
            st.subheader("Supplier Details")
            supplier_result = view_all_suppliers()
            supplier_df = pd.DataFrame(supplier_result, columns=["Supplier ID", "Name", "Contact", "Drugs Supplied"])
            st.dataframe(supplier_df)
        elif supplier_choice == "Delete":
            st.subheader("Delete Supplier")
            del_s_id = st.text_input("Supplier ID to Delete")
            if st.button("Delete Supplier"):
                delete_supplier(del_s_id)
                st.success(f"Supplier {del_s_id} deleted successfully")
    elif choice == "Transactions":
        st.subheader("Transaction Details")
        transaction_result = view_all_transactions()
        transaction_df = pd.DataFrame(transaction_result, columns=["Transaction ID", "Drug ID", "Customer Email", "Quantity Sold", "Total Price", "Transaction Date"])
        st.dataframe(transaction_df)
    elif choice == "About":
        st.subheader("DBMS Mini Project")
        st.subheader("By Pramukh (R22EF300)")


def getauthenicate(username, password):
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?', (username,))
    cust_password = c.fetchall()
    if cust_password:
        if cust_password[0][0] == password:
            return True
        else:
            return False
    else:
        return False


###################################################################


def customer(username, password):
    if getauthenicate(username, password):
        print("In Customer")
        st.title("Welcome to Pharmacy Store")

        st.subheader("Your Order Details")
        order_result = order_view_data(username)
        # st.write(cust_result)
        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
            st.dataframe(order_clean_df)

        drug_result = drug_view_all_data()
        print(drug_result)


        st.subheader("Drug: "+drug_result[0][0])
        dolo650 = st.slider(label="Quantity",min_value=0, max_value=5, key= 1)
        st.info("When to USE: " + str(drug_result[0][2]))


        st.subheader("Drug: " + drug_result[1][0])
        strepsils = st.slider(label="Quantity",min_value=0, max_value=5, key= 2)
        st.info("When to USE: " + str(drug_result[1][2]))

        st.subheader("Drug: " + drug_result[2][0])
        vicks = st.slider(label="Quantity",min_value=0, max_value=5, key=3)
        st.info("When to USE: " + str(drug_result[2][2]))



        if st.button(label="Buy now"):
            O_items = ""

            if int(dolo650) > 0:
                O_items += "Dolo-650,"
            if int(strepsils) > 0:
                O_items += "Strepsils,"
            if int(vicks) > 0:
                O_items += "Vicks"
            O_Qty = str(dolo650)+str(',') + str(strepsils) + str(",") + str(vicks)

            O_id = username + "#O" + str(random.randint(0,1000000))
            order_add_data(username, O_items, O_Qty, O_id)
            # Assuming you have variables for D_id, C_Email, Quantity_Sold, Total_Price, and Transaction_Date ready
            # For each drug bought, add a transaction and reduce drug quantity
            if int(dolo650) > 0:
                add_transaction(drug_result[0][4], username, dolo650, 100*dolo650)  # Example values for Total_Price
            if int(strepsils) > 0:
                add_transaction(drug_result[1][4], username, strepsils, 50*strepsils)  # Example values for Total_Price
            if int(vicks) > 0:
                add_transaction(drug_result[2][4], username, vicks, 75*vicks)  # Example values for Total_Price
            st.success("Transaction added and quantity updated successfully")

if __name__ == '__main__':
    drug_create_table()
    cust_create_table()
    order_create_table()
    create_suppliers_table()
    create_transactions_table()

    menu = ["Login", "SignUp","Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            if getauthenicate(username, password):
                customer(username, password)
            else:
                st.sidebar.warning('Wrong username or password')

    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_area("Email ID")
        with col2:
            cust_area = st.text_area("State")
        with col3:
            cust_number = st.text_area("Phone Number")

        if st.button("Signup"):
            if (cust_password == cust_password1):
                customer_add_data(cust_name,cust_password,cust_email, cust_area, cust_number,)
                st.success("Account Created!")
                st.info("Go to Login Menu to login")
            else:
                st.warning('Password dont match')
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if username == 'admin' and password == 'admin':
            admin()