"""Provides extra classes that can load data from various instruments into _SC_.DataFile type objects.

You do not need to use these classes directly, they are made available to :py:class:`Stoner.Core.Data` which
will load each of them in turn when asked to load an unknown data file.

Each class has a priority attribute that is used to determine the order in which
they are tried by :py:class:`Stoner.Core.Data` and friends where trying to load data.
High priority is run last (so is a bit of a misnomer!).

Eacg class should implement a load() method and optionally a save() method. Classes should make every effort to
positively identify that the file is one that they understand and throw a :py:exception:Stoner.Core._SC_.StonerLoadError` if not.
"""
from __future__ import print_function

__all__ = [
    "BNLFile",
    "BigBlueFile",
    "CSVFile",
    "EasyPlotFile",
    "FmokeFile",
    "GenXFile",
    "KermitPNGFile",
    "LSTemperatureFile",
    "MDAASCIIFile",
    "MokeFile",
    "OVFFile",
    "OpenGDAFile",
    "PIL",
    "PinkLibFile",
    "QDFile",
    "RasorFile",
    "RigakuFile",
    "SNSFile",
    "SPCFile",
    "TDMSFile",
    "TdmsFile",
    "VSMFile",
    "XRDFile",
]
# pylint: disable=unused-argument
import Stoner.Core as _SC_
import linecache
import re
import numpy as _np_
import csv
import os
import io
import struct
from re import split
from datetime import datetime
import numpy.ma as ma

import PIL
import PIL.PngImagePlugin as png
from .compat import python_v3, str2bytes, bytes2str

# Expand png size limits as we have big text blocks full of metadata
png.MAX_TEXT_CHUNK = 2 ** 22
png.MAX_TEXT_MEMORY = 2 ** 28


class CSVFile(_SC_.DataFile):

    """A subclass of DataFiule for loading generic deliminated text fiules without metadata."""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 128  # Rather generic file format so make it a low priority
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.csv", "*.txt"]  # Recognised filename patterns

    def _load(self, filename=None, header_line=0, data_line=1, data_delim=",", header_delim=",", **kargs):
        """Generic deliminated file loader routine.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Keyword Arguments:
            header_line (int): The line in the file that contains the column headers.
                If None, then column headers are auotmatically generated.
            data_line (int): The line on which the data starts
            data_delim (string): Thge delimiter used for separating data values
            header_delim (strong): The delimiter used for separating header values

        Returns:
            A copy of the current object after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        if header_line is not None:
            try:
                header_string = linecache.getline(self.filename, header_line + 1)
                header_string = re.sub(r'["\n]', "", header_string)
                header_string.index(header_delim)
            except (ValueError, SyntaxError):
                linecache.clearcache()
                raise _SC_.StonerLoadError("No Delimiters in header line")
            column_headers = [x.strip() for x in header_string.split(header_delim)]
        else:
            column_headers = ["Column" + str(x) for x in range(_np_.shape(self.data)[1])]
            data_line = linecache.getline(self.filename, data_line)
            try:
                data_line.index(data_delim)
            except ValueError:
                linecache.clearcache()
                raise _SC_.StonerLoadError("No delimiters in data lines")

        self.data = _np_.genfromtxt(self.filename, dtype="float", delimiter=data_delim, skip_header=data_line)
        self.column_headers = column_headers
        linecache.clearcache()
        return self

    def save(self, filename, **kargs):
        """Overrides the save method to allow CSVFiles to be written out to disc (as a mininmalist output)

        Args:
            filename (string): Fielname to save as (using the same rules as for the load routines)

        Keyword Arguments:
            deliminator (string): Record deliniminator (defaults to a comma)

        Returns:
            A copy of itself.
        """
        delimiter = kargs.pop("deliminator", ",")
        if filename is None:
            filename = self.filename
        if filename is None or (isinstance(filename, bool) and not filename):  # now go and ask for one
            filename = self.__file_dialog("w")
        with open(filename, "w") as outfile:
            spamWriter = csv.writer(outfile, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            i = 0
            spamWriter.writerow(self.column_headers)
            while i < self.data.shape[0]:
                spamWriter.writerow(self.data[i, :])
                i += 1
        self.filename = filename
        return self


class VSMFile(_SC_.DataFile):

    """Extends _SC_.DataFile to open VSM Files"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16  # Now makes a positive ID of its contents
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.fld"]  # Recognised filename patterns

    def __parse_VSM(self, header_line=3, data_line=3, header_delim=","):
        """An intrernal function for parsing deliminated data without a leading column of metadata.copy

        Keyword Arguments:
            header_line (int): The line in the file that contains the column headers.
                If None, then column headers are auotmatically generated.
            data_line (int): The line on which the data starts
            header_delim (strong): The delimiter used for separating header values

        Returns:
            Nothing, but modifies the current object.

        Note:
            The default values are configured fir read VSM data files
        """
        try:
            with io.open(self.filename, errors="ignore", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if i == 0:
                        self["Timestamp"] = line.strip()
                        check = datetime.strptime(self["Timestamp"], "%a %b %d %H:%M:%S %Y")
                        if check is None:
                            raise _SC_.StonerLoadError("Not a VSM file ?")
                    elif i == 1:
                        assert line.strip() == ""
                    elif i == 2:
                        header_string = line.strip()
                    elif i == header_line:
                        unit_string = line.strip()
                        column_headers = [
                            "{} ({})".format(h.strip(), u.strip())
                            for h, u in zip(header_string.split(header_delim), unit_string.split(header_delim))
                        ]
                    elif i > 3:
                        break
        except (ValueError, AssertionError, TypeError) as e:
            raise _SC_.StonerLoadError("Not a VSM File" + str(e.args))
        self.data = _np_.genfromtxt(
            self.filename,
            dtype="float",
            usemask=True,
            skip_header=data_line - 1,
            missing_values=["6:0", "---"],
            invalid_raise=False,
        )

        self.data = ma.mask_rows(self.data)
        cols = self.data.shape[1]
        self.data = _np_.reshape(self.data.compressed(), (-1, cols))
        self.column_headers = column_headers
        self.setas(x="H_vsm (T)", y="m (emu)")

    def _load(self, filename=None, *args, **kargs):
        """VSM file loader routine.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        self.__parse_VSM()
        return self


class BigBlueFile(CSVFile):

    """Extends CSVFile to load files from Nick Porter's old BigBlue code"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 64  # Also rather generic file format so make a lower priority
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dat", "*.iv", "*.rvt"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """Just call the parent class but with the right parameters set

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename

        super(BigBlueFile, self)._load(
            self.filename, *args, header_line=3, data_line=7, data_delim=" ", header_delim=","
        )
        if _np_.all(_np_.isnan(self.data)):
            raise _SC_.StonerLoadError("All data was NaN in Big Blue format")
        return self


class QDFile(_SC_.DataFile):

    """Extends _SC_.DataFile to load files from Quantum Design Systems - including PPMS, MPMS and SQUID-VSM"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 15  # Is able to make a positive ID of its file content, so get priority to check
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dat"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """QD system file loader routine.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        setas = {}
        i = 0
        with io.open(self.filename, "r", encoding="utf-8", errors="ignore") as f:  # Read filename linewise
            for i, line in enumerate(f):
                line = line.strip()
                if i == 0 and line != "[Header]":
                    raise _SC_.StonerLoadError("Not a Quantum Design File !")
                elif line == "[Header]" or line.startswith(";") or line == "":
                    continue
                elif "[Data]" in line:
                    break
                elif "," not in line:
                    raise _SC_.StonerLoadError("No data in file!")
                parts = [x.strip() for x in line.split(",")]
                if parts[1].split(":")[0] == "SEQUENCE FILE":
                    key = parts[1].split(":")[0].title()
                    value = parts[1].split(":")[1]
                elif parts[0] == "INFO":
                    if parts[1] == "APPNAME":
                        parts[1], parts[2] = parts[2], parts[1]
                    if len(parts) > 2:
                        key = "{}.{}".format(parts[0], parts[2])
                    else:
                        raise _SC_.StonerLoadError("No data in file!")
                    key = key.title()
                    value = parts[1]
                elif parts[0] in ["BYAPP", "FILEOPENTIME"]:
                    key = parts[0].title()
                    value = " ".join(parts[1:])
                elif parts[0] == "FIELDGROUP":
                    key = "{}.{}".format(parts[0], parts[1]).title()
                    value = "[{}]".format(",".join(parts[2:]))
                elif parts[0] == "STARTUPAXIS":
                    axis = parts[1][0].lower()
                    setas[axis] = setas.get(axis, []) + [int(parts[2])]
                    key = "Startupaxis-{}".format(parts[1].strip())
                    value = parts[2].strip()
                else:
                    key = parts[0] + "," + parts[1]
                    key = key.title()
                    value = " ".join(parts[2:])
                self.metadata[key] = self.metadata.string_to_type(value)
            else:
                raise _SC_.StonerLoadError("No data in file!")
            if "Byapp" not in self:
                raise _SC_.StonerLoadError("Not a Quantum Design File !")

            if python_v3:
                column_headers = f.readline().strip().split(",")
                if "," not in f.readline():
                    assert False
                    raise _SC_.StonerLoadError("No data in file!")
            else:
                column_headers = f.next().strip().split(",")
                if "," not in f.next():
                    raise _SC_.StonerLoadError("No data in file!")
            data = _np_.genfromtxt([str2bytes(l) for l in f], dtype="float", delimiter=",", invalid_raise=False)
            if data.shape[1] != len(column_headers):  # Trap for buggy QD software not giving ewnough columns of data
                data = _np_.append(
                    data, _np_.ones((data.shape[0], len(column_headers) - data.shape[1])) * _np_.NaN, axis=1
                )
            self.data = data
        self.column_headers = column_headers
        s = self.setas
        for k in setas:
            for ix in setas[k]:
                s[ix - 1] = k
        self.setas = s
        return self


class OpenGDAFile(_SC_.DataFile):

    """Extends _SC_.DataFile to load files from RASOR"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16  # Makes a positive ID of it's file type so give priority
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dat"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """Load an OpenGDA file.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        i = 0
        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if i == 0 and line != "&SRS":
                    raise _SC_.StonerLoadError("Not a GDA File from Rasor ?" + str(line))
                if "&END" in line:
                    break
                parts = line.split("=")
                if len(parts) != 2:
                    continue
                key = parts[0]
                value = parts[1].strip()
                self.metadata[key] = self.metadata.string_to_type(value)
            if python_v3:
                column_headers = f.readline().strip().split("\t")
            else:
                column_headers = f.next().strip().split("\t")
            self.data = _np_.genfromtxt([str2bytes(l) for l in f], dtype="float", invalid_raise=False)
        self.column_headers = column_headers
        return self


class RasorFile(OpenGDAFile):

    """Just an alias for OpenGDAFile"""

    pass


class SPCFile(_SC_.DataFile):

    """Extends _SC_.DataFile to load SPC files from Raman"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16  # Can't make a positive ID of itself
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.spc"]  # Recognised filename patterns

    mime_type = ["application/octet-stream"]

    def _read_xdata(self, f):
        """Read the xdata from the spc file."""
        self._pts = self._header["fnpts"]
        if self._header["ftflgs"] & 128:  # We need to read some X Data
            if 4 * self._pts > self._filesize - f.tell():
                raise _SC_.StonerLoadError("Trying to read too much data!")
            xvals = f.read(4 * self._pts)  # I think storing X vals directly implies that each one is 4 bytes....
            xdata = _np_.array(struct.unpack(str2bytes(str(self._pts) + "f"), xvals))
        else:  # Generate the X Data ourselves
            first = self._header["ffirst"]
            last = self._header["flast"]
            if self._pts > 1e6:  # Something not right here !
                raise _SC_.StonerLoadError("More than 1 million points requested. Bugging out now!")
            xdata = _np_.linspace(first, last, self._pts)
        return xdata

    def _read_ydata(self, f, data, column_headers):
        """Read the y data and column headers from spc file."""
        n = self._header["fnsub"]
        subhdr_keys = (
            "subflgs",
            "subexp",
            "subindx",
            "subtime",
            "subnext",
            "subnois",
            "subnpts",
            "subscan",
            "subwlevel",
            "subresv",
        )
        if self._header["ftflgs"] & 1:
            y_width = 2
            y_fmt = "h"
            divisor = 2 ** 16
        else:
            y_width = 4
            y_fmt = "i"
            divisor = 2 ** 32
        if n * (y_width * self._pts + 32) > self._filesize - f.tell():
            raise _SC_.StonerLoadError("No good, going to read too much data!")
        for j in range(n):  # We have n sub-scans
            # Read the subheader and import into the main metadata dictionary as scan#:<subheader item>
            subhdr = struct.unpack(b"BBHfffIIf4s", f.read(32))
            subheader = dict(zip(["scan" + str(j) + ":" + x for x in subhdr_keys], subhdr))

            # Now read the y-data
            exponent = subheader["scan" + str(j) + ":subexp"]
            if int(exponent) & -128:  # Data is unscaled direct floats
                ydata = _np_.array(struct.unpack(str2bytes(str(self._pts) + "f"), f.read(self._pts * y_width)))
            else:  # Data is scaled by exponent
                yvals = struct.unpack(str2bytes(str(self._pts) + y_fmt), f.read(self._pts * y_width))
                ydata = _np_.array(yvals, dtype="float64") * (2 ** exponent) / divisor
            data[:, j + 1] = ydata
            self._header = dict(self._header, **subheader)
            column_headers.append("Scan" + str(j) + ":" + self._yvars[self._header["fytype"]])

        return data

    def _read_loginfo(self, f):
        """Read the log info section of the spc file."""
        logstc = struct.unpack(b"IIIII44s", f.read(64))
        logstc_keys = ("logsizd", "logsizm", "logtxto", "logbins", "logdsks", "logrsvr")
        logheader = dict(zip(logstc_keys, logstc))
        self._header = dict(self._header, **logheader)

        # Can't handle either binary log information or ion disk log information (wtf is this anyway !)
        if self._header["logbins"] + self._header["logdsks"] > self._filesize - f.tell():
            raise _SC_.StonerLoadError("Too much logfile data to read")
        f.read(self._header["logbins"] + self._header["logdsks"])

        # The renishaw seems to put a 16 character timestamp next - it's not in the spec but never mind that.
        self._header["Date-Time"] = f.read(16)
        # Now read the rest of the file as log text
        logtext = f.read()
        # We expect things to be single lines terminated with a CR-LF of the format key=value
        for line in split(b"[\r\n]+", logtext):
            if b"=" in line:
                parts = line.split(b"=")
                key = parts[0].decode()
                value = parts[1].decode()
                self._header[key] = value

    def _load(self, filename=None, *args, **kargs):
        """Reads a .scf file produced by the Renishaw Raman system (amongs others)

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.

        Todo:
            Implement the second form of the file that stores multiple x-y curves in the one file.

        Notes:
            Metadata keys are pretty much as specified in the spc.h file that defines the filerformat.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        # Open the file and read the main file header and unpack into a dict
        self._filesize = os.stat(self.filename).st_size
        with io.open(filename, "rb") as f:
            spchdr = struct.unpack(b"BBBciddiBBBBi9s9sH8f30s130siiBBHf48sfifB187s", f.read(512))
            keys = (
                "ftflgs",
                "fversn",
                "fexper",
                "fexp",
                "fnpts",
                "ffirst",
                "flast",
                "fnsub",
                "fxtype",
                "fytype",
                "fztype",
                "fpost",
                "fres",
                "fsource",
                "fpeakpt",
                "fspare1",
                "fspare2",
                "fspare3",
                "fspare4",
                "fspare5",
                "fspare6",
                "fspare7",
                "fspare8",
                "fcm",
                "nt",
                "fcatx",
                "flogoff",
                "fmods",
                "fprocs",
                "flevel",
                "fsampin",
                "ffactor",
                "fmethod",
                "fzinc",
                "fwplanes",
                "fwinc",
                "fwtype",
                "fwtype",
                "fresv",
            )
            self._xvars = [
                "Arbitrary",
                "Wavenumber (cm-1)",
                "Micrometers (um)",
                "Nanometers (nm)",
                "Seconds",
                "Minutes",
                "Hertz (Hz)",
                "Kilohertz (KHz)",
                "Megahertz (MHz)",
                "Mass (M/z)",
                "Parts per million (PPM)",
                "Days",
                "Years",
                "Raman Shift (cm-1)",
                "Raman Shift (cm-1)",
                "eV",
                "XYZ text labels in fcatxt (old 0x4D version only)",
                "Diode Number",
                "Channel",
                "Degrees",
                "Temperature (F)",
                "Temperature (C)",
                "Temperature (K)",
                "Data Points",
                "Milliseconds (mSec)",
                "Microseconds (uSec)",
                "Nanoseconds (nSec)",
                "Gigahertz (GHz)",
                "Centimeters (cm)",
                "Meters (m)",
                "Millimeters (mm)",
                "Hours",
                "Hours",
            ]
            self._yvars = [
                "Arbitrary Intensity",
                "Interferogram",
                "Absorbance",
                "Kubelka-Monk",
                "Counts",
                "Volts",
                "Degrees",
                "Milliamps",
                "Millimeters",
                "Millivolts",
                "Log(1/R)",
                "Percent",
                "Percent",
                "Intensity",
                "Relative Intensity",
                "Energy",
                "Decibel",
                "Temperature (F)",
                "Temperature (C)",
                "Temperature (K)",
                "Index of Refraction [N]",
                "Extinction Coeff. [K]",
                "Real",
                "Imaginary",
                "Complex",
                "Complex",
                "Transmission (ALL HIGHER MUST HAVE VALLEYS!)",
                "Reflectance",
                "Arbitrary or Single Beam with Valley Peaks",
                "Emission",
                "Emission",
            ]

            self._header = dict(zip(keys, spchdr))
            n = self._header["fnsub"]

            if self._header["ftflgs"] & 64 == 64 or not (
                75 <= self._header["fversn"] <= 77
            ):  # This is the multiple XY curves in file flag.
                raise _SC_.StonerLoadError(
                    "Filetype not implemented yet ! ftflgs={ftflgs}, fversn={fversn}".format(**self._header)
                )
            else:  # A single XY curve in the file.
                # Read the xdata and add it to the file.
                xdata = self._read_xdata(f)
                data = _np_.zeros((self._pts, (n + 1)))  # initialise the data soace
                data[:, 0] = xdata  # Put in the X-Data
                column_headers = [self._xvars[self._header["fxtype"]]]  # And label the X column correctly

                # Now we're going to read the Y-data
                data = self._read_ydata(f, data, column_headers)
                if self._header["flogoff"] != 0:  # Ok, we've got a log, so read the log header and merge into metadata
                    self._read_loginfo(f)
            # Ok now build the Stoner._SC_.DataFile instance to return
            self.data = data
            # The next bit generates the metadata. We don't just copy the metadata because we need to figure out the typehints first - hence the loop
            # here to call _SC_.DataFile.__setitem()
            for x in self._header:
                self[x] = self._header[x]
            self.column_headers = column_headers
            if len(self.column_headers) == 2:
                self.setas = "xy"
            return self


class RigakuFile(_SC_.DataFile):

    """Loads a .ras file as produced by Rigaku X-ray diffractormeters"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16  # Can make a positive id of file from first line
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.ras"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """Reads an Rigaku ras file including handling the metadata nicely

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        from ast import literal_eval

        if filename is None or not filename:
            self.get_filename("rb")
        else:
            self.filename = filename
        sh = re.compile(r"^\*([^\s]+)\s+(.*)$")  # Regexp to grab the keys
        ka = re.compile(r"(.*)\-(\d+)$")
        header = dict()
        i = 0
        with io.open(self.filename, "rb") as f:
            for i, line in enumerate(f):
                line = bytes2str(line).strip()
                if i == 0 and line != "*RAS_DATA_START":
                    raise _SC_.StonerLoadError("Not a Rigaku file!")
                if line == "*RAS_HEADER_START":
                    break
            i2 = None
            for i2, line in enumerate(f):
                line = bytes2str(line).strip()
                m = sh.match(line)
                if m:
                    key = m.groups()[0].lower().replace("_", ".")
                    try:
                        value = m.groups()[1].decode("utf-8", "ignore")
                    except AttributeError:
                        value = m.groups()[1]
                    header[key] = value
                if "*RAS_INT_START" in line:
                    break
            keys = list(header.keys())
            keys.sort()
            for key in keys:
                m = ka.match(key)
                value = header[key].strip()
                try:
                    newvalue = literal_eval(value.strip('"'))
                except Exception:
                    newvalue = literal_eval(value)
                if m:
                    key = m.groups()[0]
                    if key in self.metadata and not (isinstance(self[key], (_np_.ndarray, list))):
                        if isinstance(self[key], str):
                            self[key] = list([self[key]])
                        else:
                            self[key] = _np_.array(self[key])
                    if key not in self.metadata:
                        if isinstance(newvalue, str):
                            self[key] = list([newvalue])
                        else:
                            self[key] = _np_.array([newvalue])
                    else:
                        if isinstance(self[key][0], str) and isinstance(self[key], list):
                            self[key].append(newvalue)
                        else:
                            self[key] = _np_.append(self[key], newvalue)
                else:
                    self.metadata[key] = newvalue

        with io.open(self.filename, "rb") as data:
            self.data = _np_.genfromtxt(
                data, dtype="float", delimiter=" ", invalid_raise=False, comments="*", skip_header=i + i2 + 1
            )
        column_headers = ["Column" + str(i) for i in range(self.data.shape[1])]
        column_headers[0:2] = [self.metadata["meas.scan.unit.x"], self.metadata["meas.scan.unit.y"]]
        for key in self.metadata:
            if isinstance(self[key], list):
                self[key] = _np_.array(self[key])
        self.setas = "xy"
        self.column_headers = column_headers
        return self

    def to_Q(self, l=1.540593):
        """Adds an additional function to covert an angualr scale to momentum transfer.

        Returns:
            a copy of itself.
        """
        self.add_column(
            (4 * _np_.pi / l) * _np_.sin(_np_.pi * self.column(0) / 360), header="Momentum Transfer, Q ($\\AA$)"
        )


class XRDFile(_SC_.DataFile):

    """Loads Files from a Brucker D8 Discovery X-Ray Diffractometer"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16  # Makes a positive id of its file contents
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dql"]  # Recognised filename patterns

    def __init__(self, *args, **kargs):
        """Add a public attribute to XRD File."""
        super(XRDFile, self).__init__(*args, **kargs)
        self._public_attrs = {"four_bounce": bool}

    def _load(self, filename=None, *args, **kargs):
        """Reads an XRD _SC_.DataFile as produced by the Brucker diffractometer

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.

        Notes:
            Format is ini file like but not enough to do standard inifile processing - in particular
            one can have multiple sections with the same name (!)
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        sh = re.compile(r"\[(.+)\]")  # Regexp to grab section name
        with io.open(self.filename, errors="ignore", encoding="utf-8") as f:  # Read filename linewise
            if f.readline().strip() != ";RAW4.00":  # Check we have the corrrect fileformat
                raise _SC_.StonerLoadError("File Format Not Recognized !")
            drive = 0
            for line in f:  # for each line
                m = sh.search(line)
                if m:  # This is a new section
                    section = m.group(1)
                    if section == "Drive":  # If this is a Drive section we need to know which Drive Section it is
                        section = section + str(drive)
                        drive = drive + 1
                    elif section == "Data":  # Data section contains the business but has a redundant first line
                        if python_v3:
                            f.readline()
                        else:
                            f.next()
                    for line in f:  # Now start reading lines in this section...
                        if (
                            line.strip() == ""
                        ):  # A blank line marks the end of the section, so go back to the outer loop which will handle a new section
                            break
                        elif section == "Data":  # In the Data section read lines of data value,vale
                            parts = line.split(",")
                            angle = parts[0].strip()
                            counts = parts[1].strip()
                            dataline = _np_.array([float(angle), float(counts)])
                            self.data = _np_.append(self.data, dataline)
                        else:  # Other sections contain metadata
                            parts = line.split("=")
                            key = parts[0].strip()
                            data = parts[1].strip()
                            # Keynames in main metadata are section:key - use the_SC_.DataFile magic to do type determination
                            self[section + ":" + key] = self.metadata.string_to_type(data)
            column_headers = ["Angle", "Counts"]  # Assume the columns were Angles and Counts

        self.data = _np_.reshape(self.data, (-1, 2))
        self.setas = "xy"
        self.four_bounce = self["HardwareConfiguration:Monochromator"] == 1
        self.column_headers = column_headers
        return self

    def to_Q(self, l=1.540593):
        """Adds an additional function to covert an angualr scale to momentum transfer

        returns a copy of itself.
        """
        self.add_column(
            (4 * _np_.pi / l) * _np_.sin(_np_.pi * self.column(0) / 360), header="Momentum Transfer, Q ($\\AA$)"
        )


class BNLFile(_SC_.DataFile):

    """
    Creates BNLFile a subclass of _SC_.DataFile that caters for files in the SPEC format given by BNL (specifically u4b beamline but hopefully generalisable).

    Author Rowan 12/2011

    The file from BNL must be split into seperate scan files before Stoner can use
    them, a separate python script has been written for this and should be found
    in data/Python/PythonCode/scripts.
    """

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 64
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.txt"]  # Recognised filename patterns

    def __init__(self, *params):
        """Constructor modification.

        Do a normal initiation using the parent class 'self' followed by adding an extra attribute line_numbers,
        line_numbers is a list of important line numbers in the file.
        I've left it open for someone to add options for more args if they wish.
        """
        super(BNLFile, self).__init__(*params)
        self.line_numbers = []

    def __find_lines(self):
        """Returns an array of ints [header_line,data_line,scan_line,date_line,motor_line]."""
        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as fp:
            self.line_numbers = [0, 0, 0, 0, 0]
            counter = 0
            for line in fp:
                counter += 1
                if counter == 1 and line[0] != "#":
                    raise _SC_.StonerLoadError("Not a BNL File ?")
                if len(line) < 2:
                    continue  # if there's nothing written on the line go to the next
                elif line[0:2] == "#L":
                    self.line_numbers[0] = counter
                elif line[0:2] == "#S":
                    self.line_numbers[2] = counter
                elif line[0:2] == "#D":
                    self.line_numbers[3] = counter
                elif line[0:2] == "#P":
                    self.line_numbers[4] = counter
                elif line[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    self.line_numbers[1] = counter
                    break

    def __get_metadata(self):
        """Load metadta from file.

        Metadata found is scan number 'Snumber', scan type and parameters 'Stype',
        scan date/time 'Sdatetime' and z motor position 'Smotor'.
        """
        scanLine = linecache.getline(self.filename, self.line_numbers[2])
        dateLine = linecache.getline(self.filename, self.line_numbers[3])
        motorLine = linecache.getline(self.filename, self.line_numbers[4])
        self.__setitem__("Snumber", scanLine.split()[1])
        tmp = "".join(scanLine.split()[2:])
        self.__setitem__("Stype", "".join(tmp.split(",")))  # get rid of commas
        self.__setitem__("Sdatetime", dateLine[3:-1])  # don't want \n at end of line so use -1
        self.__setitem__("Smotor", motorLine.split()[3])

    def __parse_BNL_data(self):
        """Internal function for parsing BNL data.

         The meta data is labelled by #L type tags
        so easy to find but #L must be excluded from the result.
        """
        self.__find_lines()
        # creates a list, line_numbers, formatted [header_line,data_line,scan_line,date_line,motor_line]
        header_string = linecache.getline(self.filename, self.line_numbers[0])
        header_string = re.sub(r'["\n]', "", header_string)  # get rid of new line character
        header_string = re.sub(r"#L", "", header_string)  # get rid of line indicator character
        column_headers = map(lambda x: x.strip(), header_string.split())
        self.__get_metadata()
        try:
            self.data = _np_.genfromtxt(self.filename, skip_header=self.line_numbers[1] - 1)
        except IOError:
            self.data = _np_.array([0])
            print("Did not import any data for {}".format(self.filename))
        self.column_headers = column_headers

    def _load(self, filename, *args, **kargs):  # fileType omitted, implicit in class call
        """BNLFile.load(filename)

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.

        Notes:
            Overwrites load method in _SC_.DataFile class, no header positions and data
            positions are needed because of the hash title structure used in BNL files.

            Normally its good to use _parse_plain_data method from _SC_.DataFile class
            to load data but unfortunately Brookhaven data isn't very plain so there's
            a new method below.
        """
        self.filename = filename
        self.__parse_BNL_data()  # call an internal function rather than put it in load function
        linecache.clearcache()
        return self


class MokeFile(_SC_.DataFile):

    """Class that extgends _SC_.DataFile to load files from the Leeds MOKE system."""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priotity = 16
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dat", "*.txt"]

    def _load(self, filename=None, *args, **kargs):
        """Leeds  MOKE file loader routine.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        with io.open(self.filename, mode="rb") as f:
            line = bytes2str(f.readline()).strip()
            if line != "#Leeds CM Physics MOKE":
                raise _SC_.StonerLoadError("Not a _SC_.DataFile from the Leeds MOKE")
            while line.startswith("#") or line == "":
                parts = line.split(":")
                if len(parts) > 1:
                    key = parts[0][1:]
                    data = ":".join(parts[1:]).strip()
                    self[key] = data
                line = bytes2str(f.readline()).strip()
            column_headers = [x.strip() for x in line.split(",")]
            self.data = _np_.genfromtxt(f, delimiter=",")
        self.setas = "xy.de"
        self.column_headers = column_headers
        return self


class FmokeFile(_SC_.DataFile):

    """Extends _SC_.DataFile to open Fmoke Files"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16  # Makes a positive ID check of its contents so give it priority in autoloading
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dat"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """Sheffield Focussed MOKE file loader routine.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        with io.open(self.filename, mode="rb") as f:
            try:
                value = [float(x.strip()) for x in bytes2str(f.readline()).split("\t")]
            except Exception:
                f.close()
                raise _SC_.StonerLoadError("Not an FMOKE file?")
            label = [x.strip() for x in bytes2str(f.readline()).split("\t")]
            if label[0] != "Header:":
                f.close()
                raise _SC_.StonerLoadError("Not a Focussed MOKE file !")
            del label[0]
            for k, v in zip(label, value):
                self.metadata[k] = v  # Create metatdata from first 2 lines
            column_headers = [x.strip() for x in bytes2str(f.readline()).split("\t")]
            self.data = _np_.genfromtxt(f, dtype="float", delimiter="\t", invalid_raise=False)
            self.column_headers = column_headers
        return self


class GenXFile(_SC_.DataFile):

    """Extends _SC_.DataFile for GenX Exported data."""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 64
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dat"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """Load function. File format has space delimited columns from row 3 onwards."""
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        pattern = re.compile(r'# Dataset "([^\"]*)" exported from GenX on (.*)$')
        pattern2 = re.compile(r"#\sFile\sexported\sfrom\sGenX\'s\sReflectivity\splugin")
        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as datafile:
            line = datafile.readline()
            match = pattern.match(line)
            match2 = pattern2.match(line)
            if match is not None:
                dataset = match.groups()[0]
                date = match.groups()[1]
                line = datafile.readline()
                line = datafile.readline()
                line = line[1:]
                self["date"] = date
            elif match2 is not None:
                line = datafile.readline()
                self["date"] = line.split(":")[1].strip()
                datafile.readline()
                line = datafile.readline()
                line = line[1:]
                dataset = "asymmetry"
            else:
                raise _SC_.StonerLoadError("Not a GenXFile")
        column_headers = [f.strip() for f in line.strip().split("\t")]
        self.data = _np_.genfromtxt(self.filename, skip_header=4)
        self["dataset"] = dataset
        self.setas = "xye"
        self.column_headers = column_headers
        return self


class SNSFile(_SC_.DataFile):

    """Reads the ASCII exported Poalrised Neutron Rfeflectivity reduced files from BL-4A line at the Spallation Neutron Source at Oak Ridge National Lab.

    File has a large header marked up with # prefixes which include several section is []
    Each section seems to have a slightly different format
    """

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dat"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """Load function. File format has space delimited columns from row 3 onwards."""
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename

        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as data:  # Slightly ugly text handling
            line = data.readline()
            if line.strip() != "# datafile created by QuickNXS 0.9.39":  # bug out oif we don't like the header
                raise _SC_.StonerLoadError("Not a file from the SNS BL4A line")
            for line in data:
                if line.startswith("# "):  # We're in the header
                    line = line[2:].strip()  # strip the header and whitespace

                if line.startswith("["):  # Look for a section header
                    section = line.strip().strip("[]")
                    if section == "Data":  # The Data section has one line of colum headers and then data
                        header = next(data)[2:].split("\t")
                        column_headers = [h.strip().decode("ascii", "ignore") for h in header]
                        self.data = _np_.genfromtxt(data)  # we end by reading the raw data
                    elif section == "Global Options":  # This section can go into metadata
                        for line in data:
                            line = line[2:].strip()
                            if line.strip() == "":
                                break
                            else:
                                self[line[2:10].strip()] = line[11:].strip()
                    elif (
                        section == "Direct Beam Runs" or section == "Data Runs"
                    ):  # These are constructed into lists ofg dictionaries for each file
                        sec = list()
                        header = next(data)
                        header = header[2:].strip()
                        keys = [s.strip() for s in header.split("  ") if s.strip()]
                        for line in data:
                            line = line[2:].strip()
                            if line == "":
                                break
                            else:
                                values = [s.strip() for s in line.split("  ") if s.strip()]
                                sec.append(dict(zip(keys, values)))
                        self[section] = sec
                else:  # We must still be in the opening un-labelled section of meta data
                    if ":" in line:
                        i = line.index(":")
                        key = line[:i].strip()
                        value = line[i + 1 :].strip()
                        self[key.strip()] = value.strip()
        self.column_headers = column_headers
        return self


class OVFFile(_SC_.DataFile):

    """A class that reads OOMMF vector format files and constructs x,y,z,u,v,w data.

    OVF 1 and OVF 2 files with text or binary data and only files with a meshtype rectangular are supported
    """

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.ovf"]  # Recognised filename patterns

    def _read_uvwdata(self, filename, fmt, lineno):
        """Read the numerical data taking account of the format."""
        if fmt == "Text":
            uvwdata = _np_.genfromtxt(self.filename, skip_header=lineno + 2)
        elif fmt == "Binary 4":
            if self["version"] == 1:
                dt = _np_.dtype(">f4")
            else:
                dt = _np_.dtype("<f4")
            with io.open(filename, "rb") as bindata:
                bindata.seek(self._ptr)
                uvwdata = _np_.fromfile(
                    bindata, dtype=dt, count=1 + self["xnodes"] * self["ynodes"] * self["znodes"] * self["valuedim"]
                )
                assert uvwdata[0] == 1234567.0, "Binary 4 format check value incorrect ! Actual Value was {}".format(
                    uvwdata[0]
                )
            uvwdata = uvwdata[1:]
            uvwdata = _np_.reshape(uvwdata, (-1, self["valuedim"]))
        elif fmt == "Binary 8":
            if self["version"] == 1:
                dt = _np_.dtype(">f8")
            else:
                dt = _np_.dtype("<f8")
            with io.open(filename, "rb") as bindata:
                bindata.seek(self._ptr)
                uvwdata = _np_.fromfile(
                    bindata, dtype=dt, count=1 + self["xnodes"] * self["ynodes"] * self["znodes"] * self["valuedim"]
                )
                assert (
                    uvwdata[0] == 123456789012345.0
                ), "Binary 4 format check value incorrect ! Actual Value was {}".format(uvwdata[0])
            uvwdata = _np_.reshape(uvwdata, (-1, self["valuedim"]))
        else:
            raise _SC_.StonerLoadError("Unknow OVF Format {}".format(fmt))
        return uvwdata

    def _load(self, filename=None, *args, **kargs):
        """Load function. File format has space delimited columns from row 3 onwards."""
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename

        self._ptr = 0
        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as data:  # Slightly ugly text handling
            line = next(data)
            self._ptr += len(line)
            line = line.strip()
            if "OOMMF: rectangular mesh" in line:
                if "v1.0" in line:
                    self["version"] = 1
                elif "v2.0" in line:
                    self["version"] = 2
                else:
                    raise _SC_.StonerLoadError("Cannot determine version of OOMMFF file")
            else:  # bug out oif we don't like the header
                raise _SC_.StonerLoadError("Not n OOMMF OVF File: opening line eas {}".format(line))
            pattern = re.compile(r"#\s*([^\:]+)\:\s+(.*)$")
            i = None
            for i, line in enumerate(data):
                self._ptr += len(line)
                line.strip()
                if line.startswith("# Begin: Data"):  # marks the start of the trext
                    break
                elif line.startswith("# Begin:") or line.startswith("# End:"):
                    continue
                else:
                    res = pattern.match(line)
                    if res is not None:
                        key = res.group(1)
                        val = res.group(2)
                        self[key] = self.metadata.string_to_type(val)
                    else:
                        raise _SC_.StonerLoadError("Failed to understand metadata")
            fmt = re.match(r".*Data\s+(.*)", line).group(1).strip()
            assert (
                self["meshtype"] == "rectangular"
            ), "Sorry only OVF files with rectnagular meshes are currently supported."
            if self["version"] == 1:
                if self["meshtype"] == "rectangular":
                    self["valuedim"] = 3
                else:
                    self["valuedim"] = 6
            uvwdata = self._read_uvwdata(filename, fmt, i)

        x = (_np_.linspace(self["xmin"], self["xmax"], self["xnode"] + 1)[:-1] + self["xbase"]) * 1e9
        y = (_np_.linspace(self["ymin"], self["ymax"], self["ynode"] + 1)[:-1] + self["ybase"]) * 1e9
        z = (_np_.linspace(self["zmin"], self["zmax"], self["znode"] + 1)[:-1] + self["zbase"]) * 1e9
        (y, z, x) = (_np_.ravel(i) for i in _np_.meshgrid(y, z, x))
        self.data = _np_.column_stack((x, y, z, uvwdata))
        column_headers = ["X (nm)", "Y (nm)", "Z (nm)", "U", "V", "W"]
        self.setas = "xyzuvw"
        self.column_headers = column_headers
        return self


class MDAASCIIFile(_SC_.DataFile):

    """Reads files generated from the APS."""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.txt"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """Load function. File format has space delimited columns from row 3 onwards."""
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        i = [0, 0, 0, 0]
        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as data:  # Slightly ugly text handling
            for i[0], line in enumerate(data):
                if (
                    i[0] == 0 and line.strip() != "## mda2ascii 1.2 generated output"
                ):  # bug out oif we don't like the header
                    raise _SC_.StonerLoadError("Not a file mda2ascii")
                line.strip()
                if "=" in line:
                    parts = line[2:].split("=")
                    self[parts[0].strip()] = self.metadata.string_to_type("".join(parts[1:]).strip())
                elif line.startswith("#  Extra PV:"):
                    # Onto the next metadata bit
                    break
            pvpat = re.compile(r"^#\s+Extra\s+PV\s\d+\:(.*)")
            for i[1], line in enumerate(data):
                if line.strip() == "":
                    continue
                elif line.startswith("# Extra PV"):
                    res = pvpat.match(line)
                    bits = [b.strip().strip(r'"') for b in res.group(1).split(",")]
                    if bits[1] == "":
                        key = bits[0]
                    else:
                        key = bits[1]
                    if len(bits) > 3:
                        key = key + " ({})".format(bits[3])
                    self[key] = self.metadata.string_to_type(bits[2])
                else:
                    break  # End of Extra PV stuff
            else:
                raise _SC_.StonerLoadError("Overran Extra PV Block")
            for i[2], line in enumerate(data):
                line.strip()
                if line.strip() == "":
                    continue
                elif line.startswith("# Column Descriptions:"):
                    break  # Start of column headers now
                elif "=" in line:
                    parts = line[2:].split("=")
                    self[parts[0].strip()] = self.metadata.string_to_type("".join(parts[1:]).strip())
            else:
                raise _SC_.StonerLoadError("Overran end of scan header before column descriptions")
            colpat = re.compile(r"#\s+\d+\s+\[([^\]]*)\](.*)")
            column_headers = []
            for i[3], line in enumerate(data):
                res = colpat.match(line)
                line.strip()
                if line.strip() == "":
                    continue
                elif line.startswith("# 1-D Scan Values"):
                    break  # Start of data
                elif res is not None:
                    if "," in res.group(2):
                        bits = [b.strip() for b in res.group(2).split(",")]
                        if bits[-2] == "":
                            colname = bits[0]
                        else:
                            colname = bits[-2]
                        if bits[-1] != "":
                            colname += " ({})".format(bits[-1])
                        if colname in column_headers:
                            colname = "{}:{}".format(bits[0], colname)
                    else:
                        colname = res.group(1).strip()
                    column_headers.append(colname)
            else:
                raise _SC_.StonerLoadError("Overand the end of file without reading data")
        self.data = _np_.genfromtxt(self.filename, skip_header=sum(i))  # so that's ok then !
        self.column_headers = column_headers
        return self


class LSTemperatureFile(_SC_.DataFile):

    """A class that reads and writes Lakeshore Temperature Calibration Curves.

    .. warning::

        This class works for cernox curves in Log Ohms/Kelvin and Log Ohms/Log Kelvin. It may or may not work with any
        other temperature calibration data !

    """

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.340"]

    def _load(self, filename=None, *args, **kargs):
        """Data loader function for 340 files."""
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename

        with io.open(self.filename, "rb") as data:
            keys = []
            vals = []
            for line in data:
                line = bytes2str(line)
                if line.strip() == "":
                    break
                parts = [p.strip() for p in line.split(":")]
                if len(parts) != 2:
                    raise _SC_.StonerLoadError("Header doesn't contain two parts at {}".format(line.strip()))
                else:
                    keys.append(parts[0])
                    vals.append(parts[1])
            else:
                raise _SC_.StonerLoadError("Overan the end of the file")
            if keys != [
                "Sensor Model",
                "Serial Number",
                "Data Format",
                "SetPoint Limit",
                "Temperature coefficient",
                "Number of Breakpoints",
            ]:
                raise _SC_.StonerLoadError("Header did not contain recognised keys.")
            for (k, v) in zip(keys, vals):
                v = v.split()[0]
                self.metadata[k] = self.metadata.string_to_type(v)
            headers = bytes2str(next(data)).strip().split()
            column_headers = headers[1:]
            dat = _np_.genfromtxt(data)
            self.data = dat[:, 1:]
        self.column_headers = column_headers
        return self

    def save(self, filename=None):
        """Overrides the save method to allow CSVFiles to be written out to disc (as a mininmalist output)

        Args:
            filename (string): Filename to save as (using the same rules as for the load routines)

        Keyword Arguments:
            deliminator (string): Record deliniminator (defaults to a comma)

        Returns:
            A copy of itself.
        """
        if filename is None:
            filename = self.filename
        if filename is None or (isinstance(filename, bool) and not filename):  # now go and ask for one
            filename = self.__file_dialog("w")
        if self.shape[1] == 2:  # 2 columns, let's hope they're the right way round!
            cols = [0, 1]
        elif (
            self.setas.has_xcol and self.setas.has_ycol
        ):  # Use ycol, x col but assume x is real temperature and y is resistance
            cols = [self.setas.ycol[0], self.setas.xcol]
        else:
            cols = range(self.shape[1])
        with io.open(filename, "w", errors="ignore", encoding="utf-8", newline="\r\n") as f:
            for k, v in (
                ("Sensor Model", "CX-1070-SD"),
                ("Serial Number", "Unknown"),
                ("Data Format", 4),
                ("SetPoint Limit", 300.0),
                ("Temperature coefficient", 1),
                ("Number of Breakpoints", len(self)),
            ):
                if k in ["Sensor Model", "Serial Number", "Data Format", "SetPoint Limit"]:
                    kstr = "{:16s}".format(k + ":")
                else:
                    kstr = "{}:   ".format(k)
                v = self.get(k, v)
                if k == "Data Format":
                    units = ["()", "()", "()", "()", "(Log Ohms/Kelvin)", "(Log Ohms/Log Kelvin)"]
                    vstr = "{}      {}".format(v, units[int(v)])
                elif k == "SetPointLimit":
                    vstr = "{}      (Kelvin)".format(v)
                elif k == "Temperature coefficient":
                    vstr = "{} {}".format(v, ["(positive)", "(negative)"][v])
                elif k == "Number of Breakpoints":
                    vstr = str(len(self))
                else:
                    vstr = str(v)
                f.write(u"{}{}\n".format(kstr, vstr))
            f.write(u"\n")
            f.write(u"No.   ")
            for i in cols:
                f.write(u"{:11s}".format(self.column_headers[i]))
            f.write(u"\n\n")
            for i in range(
                len(self.data)
            ):  # This is a slow way to write the data, but there should only ever be 200 lines
                line = "\t".join(["{:<10.8f}".format(n) for n in self.data[i, cols]])
                f.write(u"{}\t".format(i))
                f.write(u"{}\n".format(line))
        self.filename = filename
        return self


class EasyPlotFile(_SC_.DataFile):

    """A class that will extract as much as it can from an EasyPlot save File."""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 32  # Fairly generic, but can do some explicit testing

    def _load(self, filename, *args, **kargs):
        """Private loader method."""
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename

        datastart = -1
        dataend = -1

        i = 0
        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as data:
            if "******** EasyPlot save file ********" not in data.read(1024):
                raise _SC_.StonerLoadError("Not an EasyPlot Save file?")
            else:
                data.seek(0)
            for i, line in enumerate(data):
                line = line.strip()
                if line == "":
                    continue
                if line[0] not in "-0123456789" and datastart > 0 and dataend < 0:
                    dataend = i
                if line.startswith('"') and ":" in line:
                    parts = [x.strip() for x in line.strip('"').split(":")]
                    self[parts[0]] = self.metadata.string_to_type(":".join(parts[1:]))
                elif line.startswith("/"):  # command
                    parts = [x.strip('"') for x in next(csv.reader([line], delimiter=" ")) if x != ""]
                    cmd = parts[0].strip("/")
                    if len(cmd) > 1:
                        cmdname = "_{}_cmd".format(cmd)
                        if cmdname in dir(self):  # If this command is implemented as a function run it
                            cmd = getattr(self, "_{}_cmd".format(cmd))
                            cmd(parts[1:])
                        else:
                            if len(parts[1:]) > 1:
                                cmd = cmd + "." + parts[1]
                                value = ",".join(parts[2:])
                            elif len(parts[1:]) == 1:
                                value = parts[1]
                            else:
                                value = True
                            self[cmd] = value
                elif line[0] in "-0123456789" and datastart < 0:  # start of data
                    datastart = i
                    if "," in line:
                        delimiter = ","
                    else:
                        delimiter = None
        if dataend < 0:
            dataend = i
        self.data = _np_.genfromtxt(self.filename, skip_header=datastart, skip_footer=i - dataend, delimiter=delimiter)
        if self.data.shape[1] == 2:
            self.setas = "xy"
        return self

    def _extend_columns(self, i):
        """Ensure the column headers are at least i long."""
        if len(self.column_headers) < i:
            l = len(self.column_headers)
            self.data = _np_.append(
                self.data, _np_.zeros((self.shape[0], i - l)), axis=1
            )  # Need to expand the array first
            self.column_headers.extend(["Column {}".format(x) for x in range(l, i)])

    def _et_cmd(self, parts):
        """Handle axis labellling command."""
        if parts[0] == "x":
            self._extend_columns(1)
            self.column_headers[0] = parts[1]
        elif parts[0] == "y":
            self._extend_columns(2)
            self.column_headers[1] = parts[1]
        elif parts[0] == "g":
            self["title"] = parts[1]

    def _td_cmd(self, parts):
        self.setas = parts[0]

    def _sa_cmd(self, parts):
        """The sa (set-axis?) command."""
        if parts[0] == "l":  # Legend
            col = int(parts[2])
            self._extend_columns(col + 1)
            self.column_headers[col] = parts[1]


class PinkLibFile(_SC_.DataFile):

    """Extends _SC_.DataFile to load files from MdV's PINK library - as used by the GMR anneal rig."""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 32  # reasonably generic format
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.dat"]  # Recognised filename patterns

    def _load(self, filename=None, *args, **kargs):
        """File loader for PinkLib.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as f:  # Read filename linewise
            if "PINKlibrary" not in f.readline():
                raise _SC_.StonerLoadError("Not a PINK file")
            f = f.readlines()
            happened_before = False
            for i, line in enumerate(f):
                if line[0] != "#" and not happened_before:
                    header_line = i - 2  # -2 because there's a commented out data line
                    happened_before = True
                    continue  # want to get the metadata at the bottom of the file too
                elif any(s in line for s in ("Start time", "End time", "Title")):
                    tmp = line.strip("#").split(":")
                    self.metadata[tmp[0].strip()] = ":".join(tmp[1:]).strip()
            column_headers = f[header_line].strip("#\t ").split("\t")
        data = _np_.genfromtxt(self.filename, dtype="float", delimiter="\t", invalid_raise=False, comments="#")
        self.data = data[:, 0:-2]  # Deal with an errant tab at the end of each line
        self.column_headers = column_headers
        if _np_.all([h in column_headers for h in ("T (C)", "R (Ohm)")]):
            self.setas(x="T (C)", y="R (Ohm)")
        return self


class BirgeIVFile(_SC_.DataFile):

    """Implements the IV File format used by the Birge Group in Michigan State University Condesned Matter Physiscs."""

    patterns = ["*.dat"]

    def _load(self, filename=None, *args, **kargs):
        """File loader for PinkLib.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        ix = 0
        with io.open(self.filename, "r", errors="ignore", encoding="utf-8") as f:  # Read filename linewise
            if not re.compile(r"\d{1,2}/\d{1,2}/\d{4}").match(f.readline()):
                raise _SC_.StonerLoadError("Not a BirgeIVFile as no date on first line")
            data = f.readlines()
            expected = ["Vo(-))", "Vo(+))", "Ic(+)", "Ic(-)"]
            for l, m in zip(data[-4:], expected):
                if not l.startswith(m):
                    raise _SC_.StonerLoadError("Not a BirgeIVFile as wrong footer line")
                key = l[: len(m)]
                val = l[len(m) :]
                if "STDEV" in val:
                    ix2 = val.index("STDEV")
                    key2 = val[ix2 : ix2 + 4 + len(key)]
                    val2 = val[ix2 + 4 + len(key) :]
                    self.metadata[key2] = self.metadata.string_to_type(val2.strip())
                    val = val[:ix2]
                self.metadata[key] = self.metadata.string_to_type(val.strip())
            for ix, line in enumerate(data):  # Scan the ough lines to get metadata
                if ":" in line:
                    parts = line.split(":")
                    self.metadata[parts[0].strip()] = self.metadata.string_to_type(parts[1].strip())
                elif "," in line:
                    for part in line.split(","):
                        parts = part.split(" ")
                        self.metadata[parts[0].strip()] = self.metadata.string_to_type(parts[1].strip())
                elif line.startswith("H "):
                    self.metadata["H"] = self.metadata.string_to_type(line.split(" ")[1].strip())
                else:
                    headers = [x.strip() for x in line.split(" ")]
                    break
            else:
                raise _SC_.StonerLoadError("Oops ran off the end of the file!")
        self.data = _np_.genfromtxt(filename, skip_header=ix + 2, skip_footer=4)
        self.column_headers = headers

        self.setas = "xy"
        return self


class KermitPNGFile(_SC_.DataFile):

    """Loads PNG files with additional metadata embedded in them and extracts as metadata"""

    #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
    #   .. note::
    #      Subclasses with priority<=32 should make some positive identification that they have the right
    #      file type before attempting to read data.
    priority = 16  # We're checking for a the specoific PNG signature
    #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
    # the file load/save dialog boxes.
    patterns = ["*.png"]  # Recognised filename patterns

    mime_type = "image/png"

    def _check_signature(self, filename):
        """Check that this is a PNG file and raie a _SC_.StonerLoadError if not."""
        try:
            with io.open(filename, "rb") as test:
                sig = test.read(8)
            if python_v3:
                sig = [x for x in sig]
            else:
                sig = [ord(b) for b in sig]
            if self.debug:
                print(sig)
            if sig != [137, 80, 78, 71, 13, 10, 26, 10]:
                raise _SC_.StonerLoadError("Signature mismatrch")
        except Exception:
            from traceback import format_exc

            raise _SC_.StonerLoadError("Not a PNG file!>\n{}".format(format_exc()))
        return True

    def _load(self, filename=None, *args, **kargs):
        """PNG file loader routine.

        Args:
            filename (string or bool): File to load. If None then the existing filename is used,
                if False, then a file dialog will be used.

        Returns:
            A copy of the itself after loading the data.
        """
        if filename is None or not filename:
            self.get_filename("r")
        else:
            self.filename = filename
        self._check_signature(filename)
        try:
            with PIL.Image.open(self.filename, "r") as img:
                for k in img.info:
                    self.metadata[k] = img.info[k]
                self.data = _np_.asarray(img)
        except IOError:
            raise _SC_.StonerLoadError("Unable to read as a PNG file.")

        return self

    def save(self, filename, **kargs):
        """Overrides the save method to allow KermitPNGFiles to be written out to disc

        Args:
            filename (string): Filename to save as (using the same rules as for the load routines)

        Keyword Arguments:
            deliminator (string): Record deliniminator (defaults to a comma)

        Returns:
            A copy of itself.
        """
        if filename is None:
            filename = self.filename
        if filename is None or (isinstance(filename, bool) and not filename):  # now go and ask for one
            filename = self.__file_dialog("w")

        metadata = PIL.PngImagePlugin.PngInfo()
        for k in self.metadata:
            parts = self.metadata.export(k).split("=")
            key = parts[0]
            val = str2bytes("=".join(parts[1:]))
            metadata.add_text(key, val)
        img = PIL.Image.fromarray(self.data)
        img.save(filename, "png", pnginfo=metadata)
        self.filename = filename
        return self


try:  # Optional tdms support
    from nptdms import TdmsFile

    class TDMSFile(_SC_.DataFile):

        """A first stab at writing a file that will import TDMS files"""

        #: priority (int): is the load order for the class, smaller numbers are tried before larger numbers.
        #   .. note::
        #      Subclasses with priority<=32 should make some positive identification that they have the right
        #      file type before attempting to read data.
        priority = 16  # Makes a positive ID of its file contents
        #: pattern (list of str): A list of file extensions that might contain this type of file. Used to construct
        # the file load/save dialog boxes.
        patterns = ["*.tdms"]  # Recognised filename patterns

        mime_type = "application/octet-stream"

        def _load(self, filename=None, *args, **kargs):
            """TDMS file loader routine.

            Args:
                filename (string or bool): File to load. If None then the existing filename is used,
                    if False, then a file dialog will be used.

            Returns:
                A copy of the itself after loading the data.
            """
            if filename is None or not filename:
                self.get_filename("r")
            else:
                self.filename = filename
            # Open the file and read the main file header and unpack into a dict
            try:
                f = TdmsFile(self.filename)

                column_headers = []
                data = _np_.array([])

                for grp in f.objects.keys():
                    if grp == "/":
                        pass  # skip the rooot group
                    elif grp == "/'TDI Format 1.5'":
                        metadata = f.object("TDI Format 1.5")
                        for k, v in metadata.properties.items():
                            self.metadata[k] = self.metadata.string_to_type(str(v))
                    else:
                        if f.objects[grp].has_data:
                            chnl = grp.split("/")[-1]
                            chnl.strip().strip("'")
                            column_headers.append(chnl)
                            if data.size == 0:
                                data = f.objects[grp].data
                            else:
                                data = _np_.column_stack([data, f.objects[grp].data])
                self.data = data
                self.column_headers = column_headers
            except Exception:
                from traceback import format_exc

                raise _SC_.StonerLoadError("Not a TDMS File \n{}".format(format_exc()))

            return self


except ImportError:
    pass
