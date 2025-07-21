import sys
import sqlite3
import resource.resource  # type: ignore
from PySide6.QtGui import QAction, QIcon, QCursor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
  QApplication, QMainWindow, QWidget, QVBoxLayout, 
  QPushButton, QMenu, QScrollArea, QFileDialog, 
  QInputDialog, QMessageBox, QStyleFactory, QLineEdit
)
from functools import partial
from user_data import AutoReload, StyleDefine

class Programm(QMainWindow):
  def __init__(self):
      super().__init__()
      self.conn = None
      self.cur = None
      self.file_name = None
      self.status_menu = None
      self.action_btn = None
      self.ct_folder = None
      self.app_icon = QIcon(":/app_icon.png")
      self.fld_icon = QIcon(":/folder_icon.png")
      self.file_icon = QIcon(":/file_icon.png")
      self.Start_Window()
    
  def Start_Window(self):
      self.setWindowTitle('SQLite Editor')
      self.setWindowIcon(self.app_icon)
      self.resize(600, 600)

      file_btn = self.menuBar().addMenu('Edit')
      menu_btn = self.menuBar().addMenu('Menu')
      self.action_btn = self.menuBar().addMenu('Action')

      file_open = QAction('Open File', self)
      file_new = QAction('New File', self)
      file_start = QAction('Start', self)
      main_menu = QAction('Main Menu', self)
      new_value = QAction('New Value', self)
      new_table = QAction('New Table', self)

      self.status_menu = self.statusBar()
        
      file_btn.addAction(file_open)
      file_btn.addAction(file_new)
      menu_btn.addAction(file_start)
      self.action_btn.addAction(main_menu)
      self.action_btn.addAction(new_value)
      self.action_btn.addAction(new_table)

      file_open.triggered.connect(self.read_btn)
      file_new.triggered.connect(self.read_btn)
      file_start.triggered.connect(self.start_btn)
      main_menu.triggered.connect(self.ViewFolder)
      new_table.triggered.connect(self.CreateTable)
      new_value.triggered.connect(self.CreateValue)
      self.action_btn.setEnabled(False)

  def read_btn(self):
    options = QFileDialog.Options()
    self.file_name, _ = QFileDialog.getOpenFileName(self, 'Choose SQLite file', '', 'SQLite file (*.db)', options=options)

  def start_btn(self):
    if self.file_name:
      self.conn = sqlite3.connect(self.file_name)
      self.cur = self.conn.cursor()
      self.action_btn.setEnabled(True)
      self.ViewFolder()
    else:
      self.ErrorBox("Error", "File not selected")

  def ViewFolder(self):
    widget = QWidget()
    layout = QVBoxLayout(widget)

    self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = self.cur.fetchall()
        
    self.status_menu.showMessage(f"Total Tables: {len(tables)}")

    for table in tables:
      table_name = table[0]
      fld_btn = QPushButton(table_name, self)
            
      fld_btn.setStyleSheet("text-align: left; padding-left: 0px;")
      fld_btn.setIcon(self.fld_icon)
      layout.addWidget(fld_btn)
      fld_btn.clicked.connect(partial(self.ViewFile, table_name))

      context_menu = QMenu(fld_btn)
      open_fld = QAction('Open', self)
      del_fld = QAction('Delete', self)

      open_fld.triggered.connect(partial(self.context_menu_action, table_name, 'View'))
      del_fld.triggered.connect(partial(self.DeleteFolder, table_name))
      context_menu.addAction(open_fld)
      context_menu.addAction(del_fld)

      fld_btn.setContextMenuPolicy(Qt.CustomContextMenu)
      fld_btn.customContextMenuRequested.connect(lambda _, menu=context_menu: menu.exec_(QCursor.pos()))

    scroll_area = QScrollArea(self)
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(widget)
    self.setCentralWidget(scroll_area)

  def ViewFile(self, table_name):
    self.ct_folder = table_name
    central_widget = self.centralWidget()
    widget = QWidget()
    layout = QVBoxLayout(widget)

    self.cur.execute(f"SELECT * FROM {table_name};")
    files = self.cur.fetchall()
    self.status_menu.showMessage(f"Total Values: {len(files)}")
    for file in files:
      fl_btn = QPushButton(str(file), self)
        
      fl_btn.setStyleSheet("text-align: left; padding-left: 0px;")
      fl_btn.setIcon(self.file_icon)
      layout.addWidget(fl_btn)

      context_menu = QMenu(fl_btn)
      open_fl = QAction('Open', self)
      del_fl = QAction('Delete', self)

      del_fl.triggered.connect(partial(self.DeleteFolder, table_name))
      context_menu.addAction(open_fl)
      context_menu.addAction(del_fl)

      fl_btn.setContextMenuPolicy(Qt.CustomContextMenu)
      fl_btn.customContextMenuRequested.connect(lambda _, menu=context_menu: menu.exec_(QCursor.pos()))

    scroll_area = QScrollArea(self)
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(widget)
    central_widget.setWidget(scroll_area)

  def CreateTable(self):
    text, okPressed = QInputDialog.getText(self, "Create new Table", "Name:", QLineEdit.Normal, "")
    table_name = text.strip()
    text, okPressed = QInputDialog.getText(self, "Create new Table", "Types:", QLineEdit.Normal, "")
    type_name = text.strip()
    try:
      self.cur.execute(f"CREATE TABLE {table_name} ({type_name});")
      self.conn.commit()
    except Exception as e: 
      print('Exception: ', e)
      sys.exit(1)
    if AutoReload():
      self.ViewFolder()

  def CreateValue(self):
    if self.ct_folder == None:
      self.ErrorBox("Error", "Folder not selected")
    else:
      text, okPressed = QInputDialog.getText(self, "Create new Value", "Text:", QLineEdit.Normal, "")
      values = text.split(',')
      types, okPressed = QInputDialog.getText(self, "Create new Value", "Types:", QLineEdit.Normal, "")
      try:
        self.cur.executemany(f"INSERT INTO {self.ct_folder} VALUES ({types});", [tuple(values)])
        self.conn.commit()
      except Exception as e: 
        print('Exception: ', e)
        sys.exit(1)
      if AutoReload():
        self.ViewFile(self.ct_folder)

  def DeleteFolder(self, table_name):
    self.cur.execute(f"DROP TABLE {table_name}")
    self.conn.commit()
    if AutoReload():
      self.ViewFolder()

  def ErrorBox(self, name, text):
      error_box = QMessageBox(self)
      error_box.setIcon(QMessageBox.Critical)
      error_box.setWindowTitle(name)
      error_box.setText(text)
      error_box.setStandardButtons(QMessageBox.Ok)
      error_box.exec_()

  def context_menu_action(self, table_name, action):
    print(f"Table: {table_name}, Action: {action}")

  def closeEvent(self, event):
    try:
      self.cur.close()
      self.conn.close()
    except Exception as e: 
      print('Exception: ', e)
      sys.exit(1)
    event.accept()

  def clear_window(self):
    central_widget = self.centralWidget()
    central_widget.clear()

def my_app():
  app = QApplication(sys.argv)
  window = Programm()
  window.show()
  if bool(StyleDefine()):
    app.setStyle(QStyleFactory.create(StyleDefine()))
  sys.exit(app.exec())

if __name__ == '__main__':
  my_app()
