import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent  # Store a reference to the parent MovieManagementApp instance

        self.layout = QVBoxLayout(self)

        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Enter Username")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Enter Password")

        self.login_button = QPushButton("Login")

        #self.login_button.clicked.connect(parent.open_movie_management_window)

        self.layout.addWidget(QLabel("Username:"))
        self.layout.addWidget(self.username_entry)
        self.layout.addWidget(QLabel("Password:"))
        self.layout.addWidget(self.password_entry)
        self.layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.authenticate_user)

    def authenticate_user(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        self.parent.cursor.execute("USE moviemgmt;")
        query = "SELECT username, password, type FROM users WHERE username = %s AND password = %s"
        self.parent.cursor.execute(query, (username, password))
        user = self.parent.cursor.fetchone()

        if user:
            user_type = user[2]  # Assuming type column index is 2
            if user_type == "admin":
                self.parent.enable_admin_privileges()
            else:
                self.parent.enable_user_privileges()
        else:
            QMessageBox.warning(self, 'Login Error', 'Invalid username or password')   

class MovieManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movie Management System")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)  

        movie_library_label = QLabel("Movie Library")
        movie_library_label.setAlignment(Qt.AlignCenter)
        movie_library_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(movie_library_label)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.login_widget = LoginWindow(self)
        self.stacked_widget.addWidget(self.login_widget)

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="moviemgmt"
        )
        self.cursor = self.mydb.cursor(buffered=True, named_tuple=True)

    def logout(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)
        self.logged_in_as_admin = False  # Reset admin privileges

    def enable_admin_privileges(self):
        self.logged_in_as_admin = True
        self.open_movie_management_window()

    def enable_user_privileges(self):
        self.logged_in_as_admin = False
        self.open_movie_management_window()

    def open_movie_management_window(self):
        self.movie_management_widget = QWidget()
        layout = QVBoxLayout(self.movie_management_widget)

        self.add_movie_button = QPushButton("Add Movie")
        self.add_movie_button.clicked.connect(self.open_add_movie_window)

        self.view_movie_button = QPushButton("View Movies")
        self.view_movie_button.clicked.connect(self.open_view_movies_window)

        if self.logged_in_as_admin:
            layout.addWidget(self.add_movie_button)
        layout.addWidget(self.view_movie_button)  

        layout.addWidget(self.add_movie_button)
        layout.addWidget(self.view_movie_button)

        # Create and style the logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFixedSize(100, 50)  # Set the button size
        self.logout_button.clicked.connect(self.logout)

        # Add a horizontal spacer to push the logout button to the right
        spacer_item = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addSpacerItem(spacer_item)
        layout.addWidget(self.logout_button, alignment=Qt.AlignRight | Qt.AlignBottom)  # Align the button to the right and bottom

        self.stacked_widget.addWidget(self.movie_management_widget)
        self.stacked_widget.setCurrentWidget(self.movie_management_widget) 

    def open_add_movie_window(self):

        if not self.logged_in_as_admin:
            QMessageBox.warning(self, 'Access Denied', 'Admin privileges required!')
            return
        
        self.add_movie_widget = QWidget()
        layout = QVBoxLayout(self.add_movie_widget)

        self.title_label = QLabel("Title:")
        self.title_entry = QLineEdit()
        self.genre_label = QLabel("Genre:")
        self.genre_entry = QLineEdit()
        self.release_date_label = QLabel("Release Date:")
        self.release_date_entry = QLineEdit()
        self.rating_label = QLabel("Rating(out of 10):")
        self.rating_entry = QLineEdit()
        self.lead_actor_label = QLabel("Lead Actor:")
        self.lead_actor_entry = QLineEdit()
        self.review_label = QLabel("Review:")
        self.review_entry = QTextEdit()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.save_movie_details)

        self.back_button_add = QPushButton("Back")
        self.back_button_add.clicked.connect(self.back_to_main_screen_add_movie)

        layout.addWidget(self.title_label)
        layout.addWidget(self.title_entry)
        layout.addWidget(self.genre_label)
        layout.addWidget(self.genre_entry)
        layout.addWidget(self.release_date_label)
        layout.addWidget(self.release_date_entry)
        layout.addWidget(self.rating_label)
        layout.addWidget(self.rating_entry)
        layout.addWidget(self.lead_actor_label)
        layout.addWidget(self.lead_actor_entry)
        layout.addWidget(self.review_label)
        layout.addWidget(self.review_entry)
        layout.addWidget(self.add_button)
        layout.addWidget(self.back_button_add)

        self.stacked_widget.addWidget(self.add_movie_widget)
        self.stacked_widget.setCurrentWidget(self.add_movie_widget)

    def ask_award(self, title,actor_name):
        reply = QMessageBox.question(
                self.add_movie_widget,
                'Awards',
                "Do you want to add awards for this movie?",
                QMessageBox.Yes | QMessageBox.No
                )

        if reply == QMessageBox.Yes:
            self.open_add_awards_window(title,actor_name)  # Pass the 'title' parameter
        else:
            self.back_to_main_screen_add_movie()

    def save_movie_details(self):
        title = self.title_entry.text()
        genre = self.genre_entry.text()
        release_date_text = self.release_date_entry.text()
        rating = self.rating_entry.text()
        lead_actor = self.lead_actor_entry.text()
        review = self.review_entry.toPlainText()

        self.cursor.execute("USE moviemgmt;")

        try:
            release_date = int(release_date_text)
            # Validate that the release year is within a reasonable range

            if release_date < 1800 or release_date > 3000:
                raise ValueError("Invalid year")
            
            # Check if the movie already exists
            query = "SELECT * FROM movies WHERE title = %s"
            self.cursor.execute(query, (title,))
            existing_movie = self.cursor.fetchone()

            if existing_movie:
                QMessageBox.warning(self.add_movie_widget, "Warning", "Movie already exists in the database!")
                return

            #self.cursor.execute("ALTER TABLE movies MODIFY COLUMN release_date INT;")
            query = "INSERT INTO movies (title, genre, release_date, ratings, review) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (title, genre, release_date, rating, review))
            self.mydb.commit()


            query = "SELECT * FROM actors WHERE actor_name = %s"
            self.cursor.execute(query, (lead_actor,))
            user = self.cursor.fetchone()

            if user:
                query = "INSERT INTO actors2(actor_name, movie_name) VALUES(%s, %s)"
                self.cursor.execute(query, (lead_actor, title))
                self.mydb.commit()
                QMessageBox.information(self.add_movie_widget, "Success", "Movie added to the database!")
                self.ask_award(title,lead_actor)
                self.back_to_main_screen_add_movie()
            else:
                reply = QMessageBox.question(self, 'Warning', "Actor not found in the database. Do you want to add the actor?",
                                                QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.open_add_actor_window(lead_actor, title)  # Pass both the actor's name and movie's title


        except ValueError:
            QMessageBox.warning(self.add_movie_widget, "Warning", "Please enter a valid release year.")
            return
        
        return title #this is to use in the add_actor function and open_add_actor_window function
    
    def open_add_awards_window(self, movie_title,actor_name):
        self.add_awards_widget = QWidget()
        layout = QVBoxLayout(self.add_awards_widget)

        self.award_name_label = QLabel("Award Name:")
        self.award_name_entry = QLineEdit()
        self.category_label = QLabel("Category:")
        self.category_entry = QLineEdit()
        self.year_label = QLabel("Year:")
        self.year_entry = QLineEdit()

        self.add_award_button = QPushButton("Add Award")
        self.add_award_button.clicked.connect(lambda: self.add_award(movie_title,actor_name))

        layout.addWidget(self.award_name_label)
        layout.addWidget(self.award_name_entry)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_entry)
        layout.addWidget(self.year_label)
        layout.addWidget(self.year_entry)
        layout.addWidget(self.add_award_button)

        self.stacked_widget.addWidget(self.add_awards_widget)
        self.stacked_widget.setCurrentWidget(self.add_awards_widget)

    def add_award(self, movie_title,actor_name):
        award_name = self.award_name_entry.text()
        category = self.category_entry.text()
        year = self.year_entry.text()

        # Retrieve movie_id for the given movie_title
        query = "SELECT movie_id FROM movies WHERE title = %s"
        self.cursor.execute(query, (movie_title,))
        movie_id = self.cursor.fetchone()[0]

        query = "SELECT actor_id FROM actors WHERE actor_name = %s"
        self.cursor.execute(query, (actor_name,))
        actor_id = self.cursor.fetchone()[0]

        query = "INSERT INTO awards (award_name, category, year, movie_id, actor_id) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (award_name, category, year, movie_id, actor_id))
        self.mydb.commit()

        QMessageBox.information(self.add_awards_widget, "Success", "Award added for the movie!")
        self.back_to_main_screen_add_movie()  # Return to main screen
        
    def open_add_actor_window(self, actor_name,title):
        self.add_actor_widget = QWidget()
        layout = QVBoxLayout(self.add_actor_widget)

        self.actor_name_label = QLabel("Actor Name:")
        self.actor_name_entry = QLineEdit()
        self.actor_name_entry.setText(actor_name)  # Pass the actor's name to the entry field
        self.nationality_label = QLabel("Nationality:")
        self.nationality_entry = QLineEdit()

        self.add_actor_button = QPushButton("Add Actor")
        self.add_actor_button.clicked.connect(lambda: self.add_actor(actor_name, title))

        layout.addWidget(self.actor_name_label)
        layout.addWidget(self.actor_name_entry)
        layout.addWidget(self.nationality_label)
        layout.addWidget(self.nationality_entry)
        layout.addWidget(self.add_actor_button)

        self.stacked_widget.addWidget(self.add_actor_widget)
        self.stacked_widget.setCurrentWidget(self.add_actor_widget)

    def add_actor(self, actor_name,title):
        actor_name = self.actor_name_entry.text()
        nationality = self.nationality_entry.text()

        query = "INSERT INTO actors (actor_name, nationality) VALUES (%s, %s)"
        self.cursor.execute(query, (actor_name, nationality))
        self.mydb.commit()

        query = "INSERT INTO actors2 (actor_name, movie_name) VALUES (%s, %s)"
        self.cursor.execute(query, (actor_name, title))
        self.mydb.commit()

        QMessageBox.information(self.add_actor_widget, "Success", "Actor added to the database!")
        self.ask_award(title,actor_name)
        #self.stacked_widget.setCurrentWidget(self.movie_management_widget)  # Return to the main screen

    def get_actor_info(self):
        self.cursor.execute("USE moviemgmt;")
        self.cursor.execute("SELECT DISTINCT actor_name FROM actors2;")
        actor = [actor[0] for actor in self.cursor.fetchall()]
        return actor

    def back_to_main_screen_add_movie(self):
        self.stacked_widget.setCurrentWidget(self.movie_management_widget)

    def open_view_movies_window(self):
        self.view_movies_widget = QWidget()
        layout = QVBoxLayout(self.view_movies_widget)

        self.genre_label_view = QLabel("Genre:")
        self.genre_combobox_view = QComboBox()
        genres = self.get_available_genres()
        genres.insert(0, "")
        self.genre_combobox_view.addItems(genres)

        #
        self.actor_label_view = QLabel("Filter By Actor:")
        self.actor_combobox_view = QComboBox()
        actor = self.get_actor_info()
        actor.insert(0, "")
        self.actor_combobox_view.addItems(actor)
        #

        self.filter_button_view = QPushButton("Filter")
        self.filter_button_view.clicked.connect(self.filter_movies)

        self.back_button_view = QPushButton("Back")
        self.back_button_view.clicked.connect(self.back_to_main_screen_view_movies)

        self.movies_display = QTextEdit()
        self.movies_display.setReadOnly(True)

        layout.addWidget(self.genre_label_view)
        layout.addWidget(self.genre_combobox_view)
        layout.addWidget(self.actor_label_view)
        layout.addWidget(self.actor_combobox_view)
        layout.addWidget(self.filter_button_view)
        layout.addWidget(self.movies_display)
        layout.addWidget(self.back_button_view)

        self.stacked_widget.addWidget(self.view_movies_widget)
        self.stacked_widget.setCurrentWidget(self.view_movies_widget)

    def filter_movies(self):

        #Filter for genre
        genre = self.genre_combobox_view.currentText()
        # Filter for Actors
        actor = self.actor_combobox_view.currentText()
    
        if genre :  # Check if an genre is selected
            if genre == "All Genres":
                query = "SELECT * FROM movies"
                params = ()
            else:
                query = "SELECT * FROM movies WHERE genre = %s"
                params = (genre,)  

            self.cursor.execute(query, params)
            movies = self.cursor.fetchall()

            movies_info = ""
            for movie in movies:
                movies_info += f"Title: {movie[1]}, Genre: {movie[2]}, Release Date: {movie[3]}, Rating: {movie[4]}, Review: {movie[5]}\n "

            self.movies_display.setText(movies_info)   


        if actor:  # Check if an actor is selected
            query = "SELECT * FROM actors2 WHERE actor_name = %s"
            params = (actor,)

            self.cursor.execute(query, params)
            movies = self.cursor.fetchall()

            movies_info = ""
            for movie in movies:
                # Review the fetched columns from 'actors2' table and adjust the index accordingly
                # For instance, assuming columns are actor_name (index 0) and movie_name (index 1)
                movies_info += f"Actor: {movie[0]}, Movie: {movie[1]}\n"

            self.movies_display.setText(movies_info)

        '''
        release_date = self.release_date_entry_view.text()

        if release_date:
            if genre == "All Genres":
                query += " WHERE release_date = %s"
            else:
                query += " AND release_date = %s"
            params += (release_date,)
        

        self.cursor.execute(query, params)
        movies = self.cursor.fetchall()

        movies_info = ""
        for movie in movies:
            movies_info += f"Title: {movie[1]}, Genre: {movie[2]}, Release Date: {movie[3]}\n"

        self.movies_display.setText(movies_info)

        '''

    def open_show_movies_window(self):
        self.show_movies_widget = QWidget()
        layout = QVBoxLayout(self.show_movies_widget)

        self.back_button_show = QPushButton("Back")
        self.back_button_show.clicked.connect(self.back_to_main_screen_show_movie)

        self.movies_display_show = QTextEdit()
        self.movies_display_show.setReadOnly(True)

        layout.addWidget(self.movies_display_show)
        layout.addWidget(self.back_button_show)

        self.stacked_widget.addWidget(self.show_movies_widget)
        self.stacked_widget.setCurrentWidget(self.show_movies_widget)

        self.show_movies()

    def show_movies(self):
        query = "SELECT * FROM movies"
        self.cursor.execute(query)
        movies = self.cursor.fetchall()

        movies_info = ""
        for movie in movies:
            movies_info += f"Title: {movie[1]}, Genre: {movie[2]}, Release Date: {movie[3]}\n"

        self.movies_display_show.setText(movies_info)

    def get_available_genres(self):
        self.cursor.execute("SELECT DISTINCT genre FROM movies;")
        genres = [genre[0] for genre in self.cursor.fetchall()]
        genres.insert(0, "All Genres")  # Insert "All Genres" at the beginning of the list
        return genres

    def back_to_main_screen_view_movies(self):
        self.stacked_widget.setCurrentWidget(self.movie_management_widget)

def main():
    app = QApplication(sys.argv)
    
    with open('styles.css', 'r') as f:
        app.setStyleSheet(f.read())

    window = MovieManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
