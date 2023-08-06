# Coding=ASCII
import sys
import os
import subprocess
import pandas as pd
from easyexception.exception import easyexception

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, \
     QFileDialog, QHeaderView, QTableWidgetItem

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from GeneratorControl_UI import Ui_GeneratorControlMain


def load_excel(f=None):
    """
    Load parameters from a xls file
    :param f: str, file path of the xls file.
    :return df: DataFrame, a pandas DataFrame with all the parameters
    """
    if f is None:
        f = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            "default.xls")
    df = pd.read_excel(f, index_col=0, sheet_name=None)
    df = df["INPUT"].fillna("N.A.")
    return df


class runAstraGenerator(QMainWindow, Ui_GeneratorControlMain):

    def __init__(self, parent=None):
        super(runAstraGenerator, self).__init__(parent=parent)
        self.header_labels = ["key", "description", "type", "unit", "default",
                              "set"]
        self.setupUi(self)
        self.save_filename = os.path.join(os.getcwd(), "default_gen.in")
        self.exec_path = None
        self.set_table()
        self.gen_in = ""

    def load_file_dialog(self, msg="", ftypes="All Files (*)"):
        options = QFileDialog.Options()
        # Better use system dialog. If system doesn't support one it's screwed
        #options |= QFileDialog.DontUseNativeDialog
        filename = QFileDialog.getOpenFileName(self,
            msg, "", ftypes, options=options)
        if filename[0]:
            return filename[0]
        
    def save_file_dialog(self, msg="", ftypes="Excel files (*.xls *.xlsx)"):
        filename = QFileDialog.getSaveFileName(self,
            msg, "", ftypes)
        if filename[0]:
            return filename[0]

    def set_table(self, f=None):
        self.paramTableWidget.clear()
        self.paramTableWidget.setRowCount(0)
        self.paramTableWidget.setHorizontalHeaderLabels(self.header_labels)
        hheader = self.paramTableWidget.horizontalHeader()
        hheader.resizeSection(1, 400)
        vheader = self.paramTableWidget.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        df = load_excel(f)
        for ii_row in range(len(df)):
            self.paramTableWidget.insertRow(ii_row)
            self.paramTableWidget.setItem(ii_row, 0,
                QTableWidgetItem(str(df.index[ii_row])))
            self.paramTableWidget.setItem(ii_row, 1,
                QTableWidgetItem(str(df.iloc[ii_row]["description"])))
            self.paramTableWidget.setItem(ii_row, 2,
                QTableWidgetItem(str(df.iloc[ii_row]["type"])))
            self.paramTableWidget.setItem(ii_row, 3,
                QTableWidgetItem(str(df.iloc[ii_row]["unit"])))
            self.paramTableWidget.setItem(ii_row, 4,
                QTableWidgetItem(str(df.iloc[ii_row]["default"])))
            self.paramTableWidget.setItem(ii_row, 5,
                QTableWidgetItem(str(df.iloc[ii_row]["set"]).replace("N.A.",
                                                                     "")))

    def read_table(self):
        """
        Read data from table to a dictionary.
        :return df: panda.DataFrame, dataframe representation of the
        parameter table.
        """
        num_rows = self.paramTableWidget.rowCount()
        num_cols = self.paramTableWidget.columnCount()
        df_data = {}
        for ii_row in range(num_rows):
            df_data[self.paramTableWidget.item(ii_row, 0).text()] = []
            for jj_col in range(1, num_cols):
                df_data[self.paramTableWidget.item(ii_row, 0).text()].append(
                    self.paramTableWidget.item(ii_row, jj_col).text()
                )
        df = pd.DataFrame.from_dict(df_data, orient="index",
                                    columns=self.header_labels[1:])
        return df

    def convert_table(self):
        """
        Convert the table to Astra generator format
        :return genstr: str, converted generator file string.
        """
        genstr = "!Converted by runAstraGenerator.py\n&INPUT\n"
        df = self.read_table()
        for ii_row in range(df.shape[0]):
            if df.iloc[ii_row]["set"] == "":
                continue
            elif df.iloc[ii_row]["set"] == df.iloc[ii_row]["default"]:
                continue
            else:
                keys = [df.index[ii_row]]
                des = df.iloc[ii_row]["description"]
                typ = df.iloc[ii_row]["type"]
                vals = [df.iloc[ii_row]["set"]]
                # Here the idea is to accommodate the list-type parameters
                # Put key in keys, and val in vals, then iterate on the lists
                # no matter whether it's a list already. If it's a list the key
                # will be modified to be key(i), and each val will be tested.
                if typ[:4] == "list":
                    typ = typ[5:]
                    vals = vals[0].rstrip("]").lstrip("[").split(",")
                    if len(vals) > 1:
                        keys = [keys[0] + "(%i)" % (ii + 1)
                                for ii in range(len(vals))]
                    else:
                        pass

                genstr += "\n!" + "!".join(des.split("\n")) + "\n"

                for key, val in zip(keys, vals):
                    if typ == "str":
                        genstr += key + "=" + "'%s'" % val + "\n"
                    elif typ == "bool":
                        if val.upper() in ["TRUE", "T", "1"]:
                            genstr += key + "=T\n"
                        elif val.upper() in ["FALSE", "F", "0"]:
                            genstr += key + "=F\n"
                        else:
                            easyexception("runAstraGenerator.py",
                                "convert_table(self)", "Warning",
                                "Value for a \"bool\" type parameter can only "
                                "be True, T, 1, or False, F, 0.\n"
                                "This parameter " + key + " will be skipped.")
                    elif typ == "int":
                        try:
                            if int(val) != int(float(val)):
                                easyexception("runAstraGenerator.py",
                                "convert_table(self)", "Warning",
                                "Value for " + key + " should be an int. " +
                                "However it does not look like one. " +
                                "It will be converted.")
                            genstr += key + "=%i\n" % int(val)
                        except ValueError as e:
                            easyexception("runAstraGenerator.py",
                                "convert_table(self)", "Warning",
                                str(e) + "\n" + "Value for " + key +
                                " can not be converted. Skipping.")
                    elif typ == "float":
                        genstr += key + "=%.3e\n" % float(val)
                    else:
                        easyexception("runAstraGenerator.py",
                            "convert_table(self)", "Warning",
                            "Type '%s' for " % typ + key +
                            " is unknown. Skipping.")
        genstr += "/"
        return genstr

    @pyqtSlot()
    def on_loadBtn_clicked(self):
        if self.inputPathEdit.text() != "":
            reload_reply = \
                QMessageBox.question(self, "Confirm reload",
                                     "Would you like to reload a parameter "
                                     "file? All unsaved parameters will be "
                                     "lost.", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
            if reload_reply == QMessageBox.Yes:
                self.save_filename = \
                    self.load_file_dialog("Load parameters from file",
                        "Parameter Excel Files (*.xls *.xlsx);;All Files (*)")
                self.inputPathEdit.setText(self.save_filename)
                self.set_table(self.save_filename)
            else:
                pass
        else:
            self.save_filename = \
                self.load_file_dialog("Load parameters from file",
                                       "All Files (*);;Input Files (*.in)")
            self.inputPathEdit.setText(self.save_filename)
            try:
                self.set_table(self.save_filename)
            except Exception as e:
                QMessageBox.warning(self, "File loading error!",
                                    repr(e), QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def on_findExecBtn_clicked(self):
        self.exec_path = \
            self.load_file_dialog("Locate Astra generator executable")
        self.execPathEdit.setText(self.exec_path)

    @pyqtSlot()
    def on_saveBtn_clicked(self):
        if self.inputPathEdit.text() != "":
            self.save_filename = self.inputPathEdit.text()
        else:
            self.save_filename = \
                self.save_file_dialog("Save parameter file to:")
        df = self.read_table()
        if self.save_filename:
            try:
                df.to_excel(self.save_filename, sheet_name="INPUT")
            except Exception as e:
                print("Error when saving parameters in a file:\n" + repr(e))

    @pyqtSlot()
    def on_runBtn_clicked(self):
        if self.execPathEdit.text() == "":
            QMessageBox.warning(self, "No executable",
                                "No generator executable has been specified",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            if self.inputPathEdit.text() == "":
                nosave_reply = \
                    QMessageBox.question(self, "Confirm run",
                        "Current parameters not saved, the input will be saved "
                        "automatically to the current working directory as "
                        "autogen.in. Continue?",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if nosave_reply == QMessageBox.No:
                    return
                self.gen_in = os.path.join(os.getcwd(), "autogen.in")
            else:
                self.gen_in = os.path.join(
                    os.path.dirname(self.inputPathEdit.text()),
                    ".".join(os.path.splitext(
                        os.path.split(self.inputPathEdit.text())[-1]
                    )[:-1]) + "_gen.in"
                )
            astra_str = self.convert_table()
            with open(self.gen_in, "w") as f:
                f.write(astra_str)

            # Run the Generator program and make sure the "NORRAN" is removed.
            try:
                grun = subprocess.Popen([self.execPathEdit.text(),
                    self.gen_in],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = grun.communicate(timeout=20)
                easyexception("runAstraGenerator.py",
                              "on_runBtn_clicked(self)", "Message",
                              "stdout from generator run:\n" + out.decode() +
                              "\nstderr from the run:\n" + err.decode() +
                              "\nReturn code: %s\n" % str(grun.returncode))
                if os.path.isfile(os.path.join(os.getcwd(), "NORRAN")):
                    os.remove(os.path.join(os.getcwd(), "NORRAN"))

            except Exception as e:
                easyexception("runAstraGenerator.py",
                              "on_runBtn_clicked(self)", "Warning",
                              "Error running generator. The action is not "
                              "complete. System error message: " + repr(e))

    @pyqtSlot()
    def on_exitBtn_clicked(self):
        self.close()


def main():
    app = QApplication(sys.argv)
    ui = runAstraGenerator()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
