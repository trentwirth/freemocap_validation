

from PyQt6.QtWidgets import QWidget,QVBoxLayout, QLineEdit, QPushButton ,QFormLayout, QLabel
from PyQt6.QtCore import pyqtSignal

from pathlib import Path
import json

import datetime

class SavingDataAnalysisWidget(QWidget):
    data_analysis_folder_created_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)


        self.saved_folder_name_entry = QLineEdit()
        self.saved_folder_name_entry.setMaximumWidth(200)
        self.saved_folder_name_entry.setText(datetime.datetime.now().strftime("analysis_%Y-%m-%d_%H_%M_%S"))
        
        saved_folder_name_form = QFormLayout()
        saved_folder_name_form.addRow(QLabel('ID for data analysis folder'), self.saved_folder_name_entry)
        self._layout.addLayout(saved_folder_name_form)  



        self.save_data_button = QPushButton('Save out conditions to folder')
        self.save_data_button.clicked.connect(lambda: self.save_conditions_dict(self.conditions_dictionary))
        self._layout.addWidget(self.save_data_button)

    def set_session_folder_path(self, session_folder_path):
        self.session_folder_path = session_folder_path

    def set_conditions_frames_dictionary(self, conditions_dict:dict):
        self.conditions_dictionary = conditions_dict

    def save_conditions_dict(self, conditions_dictionary:dict):
        saved_folder_name = self.saved_folder_name_entry.text()
        self.saved_data_analysis_path = self.create_folder_to_save_data(saved_folder_name)

        self.create_frame_interval_json(conditions_dictionary,self.saved_data_analysis_path)
        self.data_analysis_folder_created_signal.emit()

    def create_folder_to_save_data(self, saved_folder_name:str):

        saved_data_analysis_path = self.session_folder_path/'data_analysis'/saved_folder_name
        saved_data_analysis_path.mkdir(parents = True, exist_ok=True)

        return saved_data_analysis_path

    def create_frame_interval_json(self,conditions_dictionary:dict, save_folder_path:Path):
        json_file_name = save_folder_path/'condition_frame_intervals.json'
        out_file = open(json_file_name,'w')

        json.dump(conditions_dictionary, out_file)

