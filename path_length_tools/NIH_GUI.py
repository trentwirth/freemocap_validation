
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QApplication, QHBoxLayout,QVBoxLayout

from freemocap_utils.GUI_widgets.skeleton_view_widget import SkeletonViewWidget
from freemocap_utils.GUI_widgets.slider_widget import FrameCountSlider
from freemocap_utils.GUI_widgets.video_capture_widget import VideoCapture
from freemocap_utils.GUI_widgets.NIH_widgets.frame_marking_widget import FrameMarker
from freemocap_utils.GUI_widgets.saving_data_analysis_widget import SavingDataAnalysisWidget
from freemocap_utils.GUI_widgets.NIH_widgets.balance_assessment_widget import BalanceAssessmentWidget

from pathlib import Path
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        widget = QWidget()


        slider_and_skeleton_layout = QVBoxLayout()

        self.frame_count_slider = FrameCountSlider()
        slider_and_skeleton_layout.addWidget(self.frame_count_slider)

        self.skeleton_view_widget = SkeletonViewWidget()
        self.skeleton_view_widget.setFixedSize(self.skeleton_view_widget.size())
        slider_and_skeleton_layout.addWidget(self.skeleton_view_widget)
        
        # layout.addLayout(slider_and_skeleton_layout)

        self.camera_view_widget = VideoCapture()
        # layout.addWidget(self.camera_view_widget)
        self.camera_view_widget.setFixedSize(self.skeleton_view_widget.size())

        skeleton_plot_and_video_layout = QHBoxLayout()
        skeleton_plot_and_video_layout.addLayout(slider_and_skeleton_layout)
        skeleton_plot_and_video_layout.addWidget(self.camera_view_widget)

        layout.addLayout(skeleton_plot_and_video_layout)

        self.frame_marking_widget = FrameMarker()
        layout.addWidget(self.frame_marking_widget)
        self.frame_marking_widget.setFixedSize(640,200)

        self.saving_data_widget = SavingDataAnalysisWidget()
        # layout.addWidget(self.saving_data_widget)

        self.balance_assessment_widget = BalanceAssessmentWidget()
        layout.addWidget(self.balance_assessment_widget)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.connect_signals_to_slots()

        # self.setFixedSize(layout.sizeHint())

    def connect_signals_to_slots(self):
        self.frame_count_slider.slider.valueChanged.connect(lambda: self.skeleton_view_widget.replot(self.frame_count_slider.slider.value()))

        self.skeleton_view_widget.session_folder_loaded_signal.connect(lambda: self.frame_count_slider.set_slider_range(self.skeleton_view_widget.num_frames))
        self.skeleton_view_widget.session_folder_loaded_signal.connect(lambda: self.camera_view_widget.video_loader.videoLoadButton.setEnabled(True))
        self.skeleton_view_widget.session_folder_loaded_signal.connect(lambda: self.set_session_folder_path(self.skeleton_view_widget.session_folder_path))

        self.frame_marking_widget.conditions_dict_updated_signal.connect(lambda: self.saving_data_widget.set_conditions_frames_dictionary(self.frame_marking_widget.condition_widget_dictionary))
        self.frame_marking_widget.conditions_dict_updated_signal.connect(lambda: self.balance_assessment_widget.set_conditions_frames_dictionary(self.frame_marking_widget.condition_widget_dictionary))

        self.frame_count_slider.slider.valueChanged.connect(lambda: self.camera_view_widget.set_frame(self.frame_count_slider.slider.value()) if (self.camera_view_widget.video_loader.video_is_loaded) else NotImplemented)

    def set_session_folder_path(self,session_folder_path:Path):
        self.session_folder_path = session_folder_path
        self.camera_view_widget.video_loader.set_session_folder_path(self.skeleton_view_widget.session_folder_path)
        self.saving_data_widget.set_session_folder_path(self.skeleton_view_widget.session_folder_path)
        self.balance_assessment_widget.set_session_folder_path(self.skeleton_view_widget.session_folder_path)
    
    def set_condition_frames_dictionary(self, condition_frames_dictionary:dict):
        self.condition_frames_dictionary = condition_frames_dictionary

    

        
if __name__ == "__main__":

    app = QApplication([])
    win = MainWindow()

    win.show()
    app.exec()
