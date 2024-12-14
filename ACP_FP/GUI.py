from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import mysql.connector
import datetime
import tkinter.filedialog as filedialog
import tkinter as tk
import os
from tkinter import messagebox
from textwrap import wrap

# Window appearance
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("red.json")
app = customtkinter.CTk()
app.title("Mr. Feast - Share your recipes")
app.iconbitmap('MRF_ICON.ico')
app.geometry("800x900")
app.resizable(False, False)
#app.overrideredirect(True)

# Global variables to track current user
app.current_user = None
app.current_user_image_path = None

# Main Frames
main_frame = customtkinter.CTkFrame(app)
main_frame.pack(fill="both", expand=True)

# Sign-Up Page Frame
signup_frame = customtkinter.CTkFrame(app)

# Login Page Frame
login_frame = customtkinter.CTkFrame(app)

# Post Page Frame
post_frame = customtkinter.CTkFrame(app)

# Navbar Frame
navbar_frame = customtkinter.CTkFrame(main_frame, height=50, corner_radius=0, fg_color="#e63946")
navbar_frame.pack(side="top", fill="x")

# Navbar Title (You can customize this as per your requirement)
navbar_title_label = customtkinter.CTkLabel(navbar_frame, text="Mr. Feast", font=("Bauhaus 93", 28, "bold"), text_color="white")
navbar_title_label.place(x=330, y=10)  # Adjust the position as needed

# Main Dashboard Content
top_dash = customtkinter.CTkFrame(main_frame, fg_color="#ff4d4d", height=80, corner_radius=0)
top_dash.pack(side="top", fill="x", pady=(0, 10))


def start_drag(event):
    # Capture the mouse's starting position relative to the window
    app.offset_x = event.x_root - app.winfo_x()
    app.offset_y = event.y_root - app.winfo_y()

def dragging(event):
    # Move the window according to the mouse position
    x = event.x_root - app.offset_x
    y = event.y_root - app.offset_y
    app.geometry(f"+{x}+{y}")

# Bind mouse events to enable dragging
app.bind("<Button-1>", start_drag)  # Triggered on mouse press (left click)
app.bind("<B1-Motion>", dragging)   # Triggered on mouse movement while holding the left click


# Function to Show the Sign-Up Page
def show_signup_page():
    main_frame.pack_forget()
    login_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)


# Function to Show the Login Page
def show_login_page():
    main_frame.pack_forget()
    signup_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)


# Function to show post page
def show_post_page():
    # Ensure user is logged in
    if not app.current_user:
        print("Please log in to create a post")
        return

    main_frame.pack_forget()
    signup_frame.pack_forget()
    login_frame.pack_forget()
    post_frame.pack(fill="both", expand=True)


# Function to Return to the Dashboard
def return_to_dashboard():
    signup_frame.pack_forget()
    login_frame.pack_forget()
    post_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def logout_command():
    # Remove user label and logout button
    if hasattr(app, 'user_label'):
        app.user_label.place_forget()
    if hasattr(app, 'logout_btn'):
        app.logout_btn.place_forget()

    if hasattr(app,'post_button'):
        app.post_button.place_forget()

    #Reset current user
    app.current_user = None
    app.current_user_id = None  # Also reset the user ID
    app.current_user_image_path = None

    # Restore signup and login buttons
    signup_button.place(x=500, y=25)
    login_button.place(x=650, y=25)

    # Reload posts without delete buttons
    load_posts()

def delete_post(post_id):
    # Ensure user is logged in
    if not app.current_user:
        messagebox.showerror("Error", "Please log in to delete posts")
        return

    # Confirm deletion
    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this post?"):
        return

    try:
        with mysql.connector.connect(
                host="localhost",
                user="Hadeon",
                password="Balbal22.",
                database="MR_FEASTDB"
        ) as db:
            cursor = db.cursor()

            # First check if the post belongs to the current user
            check_query = "SELECT userID FROM posts WHERE id = %s"  # Changed postID to id
            cursor.execute(check_query, (post_id,))
            result = cursor.fetchone()

            if not result or result[0] != app.current_user_id:
                messagebox.showerror("Error", "You can only delete your own posts")
                return

            # Delete the post
            delete_query = "DELETE FROM posts WHERE id = %s"  # Changed postID to id
            cursor.execute(delete_query, (post_id,))
            db.commit()

            messagebox.showinfo("Success", "Post deleted successfully")
            load_posts()  # Refresh the feed

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")

# Define the load_posts() function first
def load_posts():
    # Clear existing posts in the feed frame
    for widget in feed_frame.winfo_children():
        widget.destroy()


    # Connect to MySQL Database
    db = mysql.connector.connect(
        host="localhost",
        user="Hadeon",
        password="Balbal22.",
        database="MR_FEASTDB"
    )
    cursor = db.cursor(dictionary=True)

    # Fetch posts
    query = """
    SELECT user.username, posts.post_date, posts.title, posts.description, posts.ingredients
    FROM posts
    JOIN user ON posts.userID = user.userID
    ORDER BY posts.post_date DESC
    """
    cursor.execute(query)
    posts = cursor.fetchall()

    if not posts:
        # Show a placeholder if no posts are available
        placeholder_label = customtkinter.CTkLabel(feed_frame, text="No posts available yet. Be the first to share a recipe!",
                                                   font=("Arial", 14))
        placeholder_label.pack(pady=20)
    else:
        for post in posts:
            # User Info
            username_label = customtkinter.CTkLabel(feed_frame, text=post['username'], font=("Arial", 14, "bold"))
            username_label.pack(anchor="w")

            # Post Date
            date_label = customtkinter.CTkLabel(feed_frame, text=post['post_date'].strftime("%Y-%m-%d %H:%M:%S"),
                                                font=("Arial", 10))
            date_label.pack(anchor="e")

            # Title
            title_label = customtkinter.CTkLabel(feed_frame, text=post['title'], font=("Arial", 16, "bold"))
            title_label.pack(anchor="w")

            # Description
            description_label = customtkinter.CTkLabel(feed_frame, text=post['description'], font=("Arial", 12), wraplength=700, justify="left")
            description_label.pack(anchor="w")

            # Ingredients
            ingredients_label = customtkinter.CTkLabel(feed_frame, text=f"Ingredients: {post['ingredients']}",
                                                       font=("Arial", 12))
            ingredients_label.pack(anchor="w")

            # Separator between posts
            separator = customtkinter.CTkLabel(feed_frame, text="------------------------", font=("Arial", 10))
            separator.pack(pady=(5, 10))

    cursor.close()
    db.close()

# Then create the feed_frame and call load_posts()
feed_frame = customtkinter.CTkScrollableFrame(main_frame)
feed_frame.pack(pady=0, expand=True, fill="both")

# Automatically load posts when the application starts
load_posts()



def update_top_dash_after_login(username):
    # Remove existing signup and login buttons
    signup_button.place_forget()
    login_button.place_forget()

    # Add username greeting
    username_label = customtkinter.CTkLabel(
        top_dash,
        text=f"Welcome, {username.title()}!",
        font=("Segoe UI", 16),
        text_color="white"
    )
    username_label.place(x=650, y=26)  # Moved further right

    # Add logout button
    logout_button = customtkinter.CTkButton(
        navbar_frame,  # Changed from top_dash to navbar_frame
        text="Logout",  # Added up arrow
        width=120,
        command=logout_command,
        corner_radius=8,
        fg_color="#ff4d4d",
        hover_color="#ff8080"
    )
    logout_button.place(x=670, y=10) # Adjusted position

    # Add post button
    post_button = customtkinter.CTkButton(
        top_dash,
        text="Create Post",
        command=show_post_page,
        width=120,
        corner_radius=8,
        fg_color="#e63946",
        hover_color="#ff8080"
    )
    post_button.place(x=500, y=26)  # Adjusted position

    app.post_button = post_button

    return username_label, logout_button



# Adding Content to the Sign-Up Page
def create_signup_page():
    # Create a container frame for better organization
    container = customtkinter.CTkFrame(signup_frame, fg_color="transparent")
    container.pack(pady=50, padx=20, expand=True)

    # Logo
    image = Image.open("MRF_LOGO.png")
    image = image.resize((120, 120))
    logo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(120, 96))
    logo_label = customtkinter.CTkLabel(container, text="", image=logo)
    logo_label.pack(pady=(0, 20))

    # Title with better styling
    signup_label = customtkinter.CTkLabel(
        container,
        text="Create an Account",
        font=("Arial", 24, "bold")
    )
    signup_label.pack(pady=(0, 20))

    # Username field
    username_frame = customtkinter.CTkFrame(container, fg_color="transparent")
    username_frame.pack(fill="x", pady=(0, 15))
    username_label = customtkinter.CTkLabel(username_frame, text="Username", font=("Arial", 14))
    username_label.pack(anchor="w")
    username_entry = customtkinter.CTkEntry(
        username_frame,
        placeholder_text="Choose a username",
        width=300,
        height=40
    )
    username_entry.pack(pady=(5, 0))

    # Email field
    email_frame = customtkinter.CTkFrame(container, fg_color="transparent")
    email_frame.pack(fill="x", pady=(0, 15))
    email_label = customtkinter.CTkLabel(email_frame, text="Email", font=("Arial", 14))
    email_label.pack(anchor="w")
    email_entry = customtkinter.CTkEntry(
        email_frame,
        placeholder_text="Enter your email",
        width=300,
        height=40
    )
    email_entry.pack(pady=(5, 0))

    # Password field
    password_frame = customtkinter.CTkFrame(container, fg_color="transparent")
    password_frame.pack(fill="x", pady=(0, 20))
    password_label = customtkinter.CTkLabel(password_frame, text="Password", font=("Arial", 14))
    password_label.pack(anchor="w")
    password_entry = customtkinter.CTkEntry(
        password_frame,
        placeholder_text="Create a password",
        show="*",
        width=300,
        height=40
    )
    password_entry.pack(pady=(5, 0))

    def submit_signup():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()

        # Basic validation
        if not username or not password or not email:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        current_datetime = datetime.datetime.now()

        try:
            # Connect to MySQL Database
            db = mysql.connector.connect(
                host="localhost",
                user="Hadeon",
                password="Balbal22.",
                database="MR_FEASTDB"
            )
            cursor = db.cursor()

            # Check if username already exists
            cursor.execute("SELECT username FROM user WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Insert user into the database
            query = "INSERT INTO user (username, password, email, account_date) VALUES (%s, %s, %s, %s)"
            values = (username.capitalize(), password, email, current_datetime)
            cursor.execute(query, values)
            db.commit()

            messagebox.showinfo("Success", "Account created successfully!")

            # Set current user
            app.current_user = username
            # Get the user ID
            cursor.execute("SELECT userID FROM user WHERE username = %s", (username,))
            result = cursor.fetchone()
            app.current_user_id = result[0]

            user_label, logout_btn = update_top_dash_after_login(username)
            app.user_label = user_label
            app.logout_btn = logout_btn

            return_to_dashboard()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

    # Sign up button
    submit_button = customtkinter.CTkButton(
        container,
        text="Create Account",
        command=submit_signup,
        width=300,
        height=40,
        font=("Arial", 14, "bold"),
        fg_color="#e63946",
        hover_color="#ff4d4d"
    )
    submit_button.pack(pady=(0, 20))

    # Back button
    back_button = customtkinter.CTkButton(
        container,
        text="Back to Home",
        command=return_to_dashboard,
        width=300,
        height=40,
        font=("Arial", 14),
        fg_color="#ff4d4d",
        hover_color="#ff4d4d",
        border_width=2,
        border_color="#e63946"
    )
    back_button.pack()


create_signup_page()


# Adding Content to the Login Page
def create_login_page():
    # Create a container frame for better organization
    container = customtkinter.CTkFrame(login_frame, fg_color="transparent")
    container.pack(pady=50, padx=20, expand=True)

    # Define submit_login function first
    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        # Check user credentials in the database
        try:
            with mysql.connector.connect(
                    host="localhost",
                    user="Hadeon",
                    password="Balbal22.",
                    database="MR_FEASTDB"
            ) as db:
                with db.cursor(dictionary=True) as cursor:
                    query = "SELECT * FROM user WHERE username = %s AND password = %s"
                    cursor.execute(query, (username, password))
                    result = cursor.fetchone()

                    if result:
                        app.current_user = username  # Set current user (username)
                        app.current_user_id = result['userID']  # Fetch and store the userID

                        user_label, logout_btn = update_top_dash_after_login(username)
                        app.user_label = user_label
                        app.logout_btn = logout_btn

                        # Load the posts to display after logging in
                        load_posts()

                        return_to_dashboard()
                    else:
                        messagebox.showerror("Login Error", "Invalid username or password")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")

    # Logo
    image = Image.open("MRF_LOGO.png")
    image = image.resize((120, 120))
    logo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(120, 96))
    logo_label = customtkinter.CTkLabel(container, text="", image=logo)
    logo_label.pack(pady=(0, 20))

    # Title with better styling
    login_label = customtkinter.CTkLabel(
        container,
        text="Welcome Back!",
        font=("Arial", 24, "bold")
    )
    login_label.pack(pady=(0, 20))

    # Username field with icon
    username_frame = customtkinter.CTkFrame(container, fg_color="transparent")
    username_frame.pack(fill="x", pady=(0, 15))
    username_label = customtkinter.CTkLabel(username_frame, text="Username", font=("Arial", 14))
    username_label.pack(anchor="w")
    username_entry = customtkinter.CTkEntry(
        username_frame,
        placeholder_text="Enter your username",
        width=300,
        height=40
    )
    username_entry.pack(pady=(5, 0))

    # Password field with icon
    password_frame = customtkinter.CTkFrame(container, fg_color="transparent")
    password_frame.pack(fill="x", pady=(0, 20))
    password_label = customtkinter.CTkLabel(password_frame, text="Password", font=("Arial", 14))
    password_label.pack(anchor="w")
    password_entry = customtkinter.CTkEntry(
        password_frame,
        placeholder_text="Enter your password",
        show="*",
        width=300,
        height=40
    )
    password_entry.pack(pady=(5, 0))

    # Login button with better styling
    submit_button = customtkinter.CTkButton(
        container,
        text="Login",
        command=submit_login,  # Now submit_login is defined before it's used
        width=300,
        height=40,
        font=("Arial", 14, "bold"),
        fg_color="#e63946",
        hover_color="#ff4d4d"
    )
    submit_button.pack(pady=(0, 20))

    # Back button
    back_button = customtkinter.CTkButton(
        container,
        text="Back to Home",
        command=return_to_dashboard,
        width=300,
        height=40,
        font=("Arial", 14),
        fg_color="#ff4d4d",
        hover_color="#ff4d4d",
        border_width=2,
        border_color="#e63946"
    )
    back_button.pack()



create_login_page()


# Create Post Page
def create_post_page():
    def clear_post_page():
        title_entry.delete(0, 'end')
        description_entry.delete('1.0', 'end')
        ingredients_entry.delete('1.0', 'end')
        app.current_user_image_path = None


    def submit_post():
        # Get post data
        title = title_entry.get()
        description = description_entry.get("1.0", tk.END).strip()
        ingredients = ingredients_entry.get("1.0", tk.END).strip()
        post_date = datetime.datetime.now()

        # Validate inputs
        if not title or not description or not ingredients:
            print("Please fill in all required fields")
            return

        # Connect to MySQL Database
        db = mysql.connector.connect(
            host="localhost",
            user="Hadeon",
            password="Balbal22.",
            database="MR_FEASTDB"
        )
        cursor = db.cursor()

        # Check if userID exists (just for safety)
        if not app.current_user_id:
            print("User ID is not available")
            return

        user_id = app.current_user_id  # Use the userID stored after login

        # Insert post into database
        query = """
        INSERT INTO posts
        (userID, title, description, ingredients, post_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (user_id, title, description, ingredients, post_date)

        try:
            cursor.execute(query, values)
            db.commit()
            print("Post created successfully!")

            # Clear the form and return to main dashboard
            clear_post_page()
            # Refresh the feed to show the new post
            load_posts()
            return_to_dashboard()
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            # Print the exact query and values for debugging
            print(f"Query: {query}")
            print(f"Values: {values}")
        finally:
            cursor.close()
            db.close()

    # Back button
    back_button = customtkinter.CTkButton(
        post_frame,
        text="Back",
        command=return_to_dashboard
    )
    back_button.pack(pady=10)

    # Title Label and Entry
    title_label = customtkinter.CTkLabel(post_frame, text="Recipe Title:")
    title_label.pack(pady=(10, 5))
    title_entry = customtkinter.CTkEntry(post_frame, width=400)
    title_entry.pack(pady=(0, 10))

    # Description Label and Textbox
    description_label = customtkinter.CTkLabel(post_frame, text="Recipe Description:")
    description_label.pack(pady=(10, 5))
    description_entry = customtkinter.CTkTextbox(post_frame, width=400, height=200)
    description_entry.pack(pady=(0, 10))

    # Ingredients Label and Textbox
    ingredients_label = customtkinter.CTkLabel(post_frame, text="Ingredients:")
    ingredients_label.pack(pady=(10, 5))
    ingredients_entry = customtkinter.CTkTextbox(post_frame, width=400, height=100)
    ingredients_entry.pack(pady=(0, 10))

    # Submit Button
    submit_button = customtkinter.CTkButton(
        post_frame,
        text="Post Recipe",
        command=submit_post
    )
    submit_button.pack(pady=20)


# Call create_post_page to set up the post page
create_post_page()



# Logo format (in navbar_frame)
image = Image.open("MRF_LOGO.png")
image = image.resize((1000, 1000))
ctk_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(60, 48))

image_label = customtkinter.CTkLabel(navbar_frame, text="", image=ctk_image)
image_label.place(x=260, y=2)  # Adjust the position for the navbar


# Search Bar
search_entry = customtkinter.CTkEntry(
    top_dash,
    placeholder_text="Search recipes...",
    width=300,
    corner_radius=8,
    font=("Helvetica", 14),
    border_width=2,
    fg_color="white",
    text_color="black"
)
search_entry.place(x=30, y=28)


def search_recipes(event=None):
    search_term = search_entry.get().strip().lower()

    # Clear existing posts
    for widget in feed_frame.winfo_children():
        widget.destroy()

    if not search_term:
        load_posts()  # If search is empty, show all posts
        return

    try:
        # Connect to MySQL Database
        db = mysql.connector.connect(
            host="localhost",
            user="Hadeon",
            password="Balbal22.",
            database="MR_FEASTDB"
        )
        cursor = db.cursor(dictionary=True)

        # Search in title, description, and ingredients
        query = """
        SELECT posts.id, posts.userID, user.username, posts.post_date, posts.title, 
               posts.description, posts.ingredients
        FROM posts
        JOIN user ON posts.userID = user.userID
        WHERE LOWER(title) LIKE %s 
           OR LOWER(description) LIKE %s 
           OR LOWER(ingredients) LIKE %s
        ORDER BY posts.post_date DESC
        """
        search_pattern = f"%{search_term}%"
        cursor.execute(query, (search_pattern, search_pattern, search_pattern))
        posts = cursor.fetchall()

        if not posts:
            # Show "No results found" message
            no_results_label = customtkinter.CTkLabel(
                feed_frame,
                text="No recipes found matching your search.",
                font=("Arial", 14)
            )
            no_results_label.pack(pady=20)
        else:
            # Display search results
            for post in posts:
                # Create a frame for each post
                post_frame = customtkinter.CTkFrame(feed_frame)
                post_frame.pack(fill="x", padx=10, pady=5)

                # Header frame
                header_frame = customtkinter.CTkFrame(post_frame)
                header_frame.pack(fill="x", padx=5, pady=2)

                # Username
                username_label = customtkinter.CTkLabel(
                    header_frame,
                    text=post['username'],
                    font=("Arial", 14, "bold")
                )
                username_label.pack(side="left", padx=5)

                # Add delete button only if user is logged in and owns the post
                if hasattr(app, 'current_user_id') and app.current_user and app.current_user_id == post['userID']:
                    delete_button = customtkinter.CTkButton(
                        header_frame,
                        text="Delete",
                        command=lambda pid=post['id']: delete_post(pid),
                        width=80,
                        height=25,
                        fg_color="#e63946",
                        hover_color="#ff4d4d"
                    )
                    delete_button.pack(side="right", padx=5)

                # Date
                date_label = customtkinter.CTkLabel(
                    header_frame,
                    text=post['post_date'].strftime("%Y-%m-%d %H:%M:%S"),
                    font=("Arial", 10)
                )
                date_label.pack(side="right", padx=5)

                # Content
                content_frame = customtkinter.CTkFrame(post_frame)
                content_frame.pack(fill="x", padx=5, pady=2)

                # Title
                title_label = customtkinter.CTkLabel(
                    content_frame,
                    text=post['title'],
                    font=("Arial", 16, "bold")
                )
                title_label.pack(anchor="w")

                # Description
                description_label = customtkinter.CTkLabel(
                    content_frame,
                    text=post['description'],
                    font=("Arial", 12)
                )
                description_label.pack(anchor="w")

                # Ingredients
                ingredients_label = customtkinter.CTkLabel(
                    content_frame,
                    text=f"Ingredients: {post['ingredients']}",
                    font=("Arial", 12)
                )
                ingredients_label.pack(anchor="w")

                # Separator
                separator = customtkinter.CTkLabel(
                    feed_frame,
                    text="------------------------",
                    font=("Arial", 10)
                )
                separator.pack(pady=(5, 10))

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()


# Bind the search function to the search entry
search_entry.bind('<Return>', search_recipes)  # Trigger search on Enter key

# Add a search button for better UX
search_button = customtkinter.CTkButton(
    top_dash,
    text="Search",
    command=search_recipes,
    width=70,
    height=32,
    corner_radius=8,
    fg_color="#e63946",
    hover_color="#ff4d4d"
)
search_button.place(x=340, y=28)  # Place next to the search entry

# Sign-Up Button placed on the top_dash
signup_button = customtkinter.CTkButton(
    top_dash,
    text="Sign Up",
    command=show_signup_page,
    width=120,
    corner_radius=8,
    fg_color="#e63946",
    hover_color="#ff8080"
)
signup_button.place(x=500, y=25)

# Login Button placed on the top_dash
login_button = customtkinter.CTkButton(
    top_dash,
    text="Login",
    command=show_login_page,
    width=120,
    corner_radius=8,
    fg_color="#e63946",
    hover_color="#ff8080"
)
login_button.place(x=650, y=25)



def load_posts():
    # Clear existing posts in the feed frame
    for widget in feed_frame.winfo_children():
        widget.destroy()

    # Connect to MySQL Database
    db = mysql.connector.connect(
        host="localhost",
        user="Hadeon",
        password="Balbal22.",
        database="MR_FEASTDB"
    )
    cursor = db.cursor(dictionary=True)

    # Updated query to include id (postID) instead of postID
    query = """
    SELECT posts.id, posts.userID, user.username, posts.post_date, posts.title, 
           posts.description, posts.ingredients
    FROM posts
    JOIN user ON posts.userID = user.userID
    ORDER BY posts.post_date DESC
    """
    cursor.execute(query)
    posts = cursor.fetchall()

    if not posts:
        placeholder_label = customtkinter.CTkLabel(
            feed_frame,
            text="No recipes found matching your search.",
            font=("Arial", 14)
        )
        placeholder_label.pack(pady=20)
    else:
        for post in posts:
            # Create a frame for each post
            post_frame = customtkinter.CTkFrame(feed_frame)
            post_frame.pack(fill="x", padx=10, pady=5)

            # Header frame for username, date, and delete button
            header_frame = customtkinter.CTkFrame(post_frame)
            header_frame.pack(fill="x", padx=5, pady=2)

            # User Info
            username_label = customtkinter.CTkLabel(
                header_frame,
                text=post['username'],
                font=("Arial", 14, "bold")
            )
            username_label.pack(side="left", padx=5)

            # Add delete button if the post belongs to current user
            if hasattr(app, 'current_user_id') and app.current_user_id == post['userID']:
                delete_button = customtkinter.CTkButton(
                    header_frame,
                    text="Delete",
                    command=lambda pid=post['id']: delete_post(pid),  # Changed postID to id
                    width=80,
                    height=25,
                    fg_color="#e63946",
                    hover_color="#ff4d4d"
                )
                delete_button.pack(side="right", padx=5)

            # Post Date
            date_label = customtkinter.CTkLabel(
                header_frame,
                text=post['post_date'].strftime("%Y-%m-%d %H:%M:%S"),
                font=("Arial", 10)
            )
            date_label.pack(side="right", padx=5)

            # Content frame
            content_frame = customtkinter.CTkFrame(post_frame)
            content_frame.pack(fill="x", padx=5, pady=2)

            # Title
            title_label = customtkinter.CTkLabel(
                content_frame,
                text=post['title'],
                font=("Arial", 16, "bold")
            )
            title_label.pack(anchor="w")

            # Description
            description_label = customtkinter.CTkLabel(
                content_frame,
                text=post['description'],
                font=("Arial", 12),
                wraplength=700,
                justify="left"
            )
            description_label.pack(anchor="w")

            # Ingredients
            ingredients_label = customtkinter.CTkLabel(
                content_frame,
                text=f"Ingredients: {post['ingredients']}",
                font=("Arial", 12)
            )
            ingredients_label.pack(anchor="w")

            # Separator between posts
            separator = customtkinter.CTkLabel(
                feed_frame,
                text="------------------------",
                font=("Arial", 10)
            )
            separator.pack(pady=(5, 10))

    cursor.close()
    db.close()




app.mainloop()
