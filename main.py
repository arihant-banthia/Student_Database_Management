import sqlite3
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication, QLabel, QWidget,\
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
# QMainWindow allows us to have division among different sections of App


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # to instantiate the parent in its method
        self.setWindowTitle(" Student Management System ")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        # used in mac only if help section is not being displayed

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        # to remove the index which we were coming left side
        self.setCentralWidget(self.table)

        # Create a toolbar and its elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)

        # create a status bar and its elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # detect a self click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        # print(list(result))
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            # print(row_data)
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300) # for dialog boxes (good practice)

        layout = QVBoxLayout()

        index = studentdata.table.currentRow()
        student_name = studentdata.table.item(index, 1).text()

        # get id from the Selected Row
        self.student_id = studentdata.table.item(index, 0).text()

        # Add Student name Widgets
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        course_name = studentdata.table.item(index, 2).text()
        # Add combo Box of Courses
        self.course_name = QComboBox()
        courses = ["Biology", "Maths", "Chemistry", "Economics", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        # the two course_name are different
        layout.addWidget(self.course_name)

        mobile = studentdata.table.item(index, 3).text()
        # add mobile widget
        self.mobile_number = QLineEdit(mobile)
        self.mobile_number.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile_number)

        # add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? "
                       "where id = ?", (self.student_name.text(),
                                      self.course_name.itemText(
                                          self.course_name.currentIndex()),
                                      self.mobile_number.text(),
                                      self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        # refresh the table
        studentdata.load_data()


class DeleteDialog(QDialog):
    pass


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300) # for dialog boxes (good practice)

        layout = QVBoxLayout()

        # Add Student name Widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo Box of Courses
        self.course_name = QComboBox()
        courses = ["Biology", "Maths", "Chemistry", "Economics", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # add mobile widget
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile_number)

        # add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) "
                       "VALUES(?, ?, ?)", (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()

        studentdata.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Set window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        row = list(result)
        print(row)
        items = studentdata.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            studentdata.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()




app = QApplication(sys.argv)
studentdata = MainWindow()
studentdata.show()
studentdata.load_data()
sys.exit(app.exec())