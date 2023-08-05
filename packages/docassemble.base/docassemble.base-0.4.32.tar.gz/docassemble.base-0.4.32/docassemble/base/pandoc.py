import os
import os.path
from six import string_types, text_type, PY2, PY3
if PY2:
    import subprocess32 as subprocess
else:
    import subprocess
import docassemble.base.filter
import docassemble.base.functions
import tempfile
import shutil
import sys
import re
import time
import random
from docassemble.base.config import daconfig
from docassemble.base.logger import logmessage
from docassemble.base.pdfa import pdf_to_pdfa
from docassemble.base.pdftk import pdf_encrypt, PDFTK_PATH, replicate_js_and_calculations
from io import open
import mimetypes
from subprocess import call, check_output
import convertapi

style_find = re.compile(r'{\s*(\\s([1-9])[^\}]+)\\sbasedon[^\}]+heading ([0-9])', flags=re.DOTALL)
PANDOC_PATH = daconfig.get('pandoc', 'pandoc')

def convertapi_to_pdf(from_file, to_file):
    convertapi.api_secret = daconfig.get('convertapi secret')
    result = convertapi.convert('pdf', { 'File': from_file })
    result.file.save(to_file)

def get_pandoc_version():
    p = subprocess.Popen(
        [PANDOC_PATH, '--version'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    version_content = p.communicate()[0].decode('utf-8')
    version_content = re.sub(r'\n.*', '', version_content)
    version_content = re.sub(r'^pandoc ', '', version_content)
    return version_content

PANDOC_INITIALIZED = False
PANDOC_OLD = False
PANDOC_ENGINE = '--pdf-engine=' + daconfig.get('pandoc engine', 'pdflatex')

def initialize_pandoc():
    if PANDOC_INITIALIZED:
        return
    global PANDOC_OLD
    global PANDOC_ENGINE
    global PANDOC_INITIALIZED
    PANDOC_VERSION = get_pandoc_version()
    if PANDOC_VERSION.startswith('1'):
        PANDOC_OLD = True
        PANDOC_ENGINE = '--latex-engine=' + daconfig.get('pandoc engine', 'pdflatex')
    else:
        PANDOC_OLD = False
        try:
            msg = subprocess.check_output(['lualatex', '--help'], stderr=subprocess.STDOUT)
            assert os.path.isfile('/usr/share/texlive/texmf-dist/tex/luatex/luatexbase/luatexbase.sty')
            lualatex_supported = True
        except:
            lualatex_supported = False
        if lualatex_supported:
            PANDOC_ENGINE = '--pdf-engine=' + daconfig.get('pandoc engine', 'lualatex')
        else:
            PANDOC_ENGINE = '--pdf-engine=' + daconfig.get('pandoc engine', 'pdflatex')
    PANDOC_INITIALIZED = True

LIBREOFFICE_PATH = daconfig.get('libreoffice', 'libreoffice')
LIBREOFFICE_MACRO_PATH = daconfig.get('libreoffice macro file', '/var/www/.config/libreoffice/4/user/basic/Standard/Module1.xba')
LIBREOFFICE_INITIALIZED = False

convertible_mimetypes = {"application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx", "application/vnd.oasis.opendocument.text": "odt"}
convertible_extensions = {"docx": "docx", "odt": "odt"}
if daconfig.get('libreoffice', 'libreoffice') is not None:
    convertible_mimetypes.update({"application/msword": "doc", "application/rtf": "rtf"})
    convertible_extensions.update({"doc": "doc", "rtf": "rtf"})

#fontfamily: zi4, mathptmx, courier
#\ttfamily
#\renewcommand{\thesubsubsubsection}{\alph{subsubsubsection}.}
#\renewcommand{\thesubsubsubsubsection}{\roman{subsubsubsubsection}.}
#  - \newenvironment{allcaps}{\startallcaps}{}
#  - \def\startallcaps#1\end{\uppercase{#1}\end}

class MyPandoc(object):
    def __init__(self, **kwargs):
        initialize_pandoc()
        if 'pdfa' in kwargs and kwargs['pdfa']:
            self.pdfa = True
        else:
            self.pdfa = False
        self.password = kwargs.get('password', None)
        self.input_content = None
        self.output_content = None
        self.input_format = 'markdown'
        self.output_format = 'rtf'
        self.output_extension = 'rtf'
        self.output_filename = None
        self.template_file = None
        self.reference_file = None
        self.metadata = dict()
        self.initial_yaml = list()
        self.additional_yaml = list()
        self.arguments = []
    def convert_to_file(self, question):
        metadata_as_dict = dict()
        if type(self.metadata) is dict:
            metadata_as_dict = self.metadata
        elif type(self.metadata) is list:
            for data in self.metadata:
                if type(data) is dict:
                    for key in data:
                        metadata_as_dict[key] = data[key]
        if self.output_format == 'rtf to docx':
            self.output_extension = 'rtf'
        else:
            self.output_extension = self.output_format
        if self.output_format in ('rtf', 'rtf to docx') and self.template_file is None:
            self.template_file = docassemble.base.functions.standard_template_filename('Legal-Template.rtf')
        if self.output_format == 'docx' and self.reference_file is None:
            self.reference_file = docassemble.base.functions.standard_template_filename('Legal-Template.docx')
        if (self.output_format == 'pdf' or self.output_format == 'tex') and self.template_file is None:
            self.template_file = docassemble.base.functions.standard_template_filename('Legal-Template.tex')
        yaml_to_use = list()
        if self.output_format in ('rtf', 'rtf to docx'):
            #logmessage("pre input content is " + str(self.input_content))
            self.input_content = docassemble.base.filter.rtf_prefilter(self.input_content, metadata=metadata_as_dict)
            #logmessage("post input content is " + str(self.input_content))
        if self.output_format == 'docx':
            self.input_content = docassemble.base.filter.docx_filter(self.input_content, metadata=metadata_as_dict, question=question)
        if self.output_format == 'pdf' or self.output_format == 'tex':
            if len(self.initial_yaml) == 0:
                standard_file = docassemble.base.functions.standard_template_filename('Legal-Template.yml')
                if standard_file is not None:
                    self.initial_yaml.append(standard_file)
            for yaml_file in self.initial_yaml:
                if yaml_file is not None:
                    yaml_to_use.append(yaml_file)
            for yaml_file in self.additional_yaml:
                if yaml_file is not None:
                    yaml_to_use.append(yaml_file)
            #logmessage("Before: " + repr(self.input_content))
            self.input_content = docassemble.base.filter.pdf_filter(self.input_content, metadata=metadata_as_dict, question=question)
            #logmessage("After: " + repr(self.input_content))
        if not re.search(r'[^\s]', self.input_content):
            self.input_content = u"\\textbf{}\n"
        if PY3:
            temp_file = tempfile.NamedTemporaryFile(prefix="datemp", mode="w", suffix=".md", delete=False, encoding='utf-8')
            temp_file.write(self.input_content)
        else:
            temp_file = tempfile.NamedTemporaryFile(prefix="datemp", mode="w", suffix=".md", delete=False)
            with open(temp_file.name, 'w', encoding='utf-8') as fp:
                fp.write(self.input_content)
        temp_file.close()
        temp_outfile = tempfile.NamedTemporaryFile(prefix="datemp", mode="wb", suffix="." + str(self.output_extension), delete=False)
        temp_outfile.close()
        current_temp_dir = 'epsconv'
        latex_conversion_directory = os.path.join(tempfile.gettempdir(), 'conv')
        if not os.path.isdir(latex_conversion_directory):
            os.makedirs(latex_conversion_directory)
        if not os.path.isdir(latex_conversion_directory):
            raise Exception("Could not create latex conversion directory")
        icc_profile_in_temp = os.path.join(tempfile.gettempdir(), 'sRGB_IEC61966-2-1_black_scaled.icc')
        if not os.path.isfile(icc_profile_in_temp):
            shutil.copyfile(docassemble.base.functions.standard_template_filename('sRGB_IEC61966-2-1_black_scaled.icc'), icc_profile_in_temp)
        subprocess_arguments = [PANDOC_PATH, PANDOC_ENGINE]
        if PANDOC_OLD:
            subprocess_arguments.append("--smart")
        subprocess_arguments.extend(['-M', 'latextmpdir=' + os.path.join('.', 'conv'), '-M', 'pdfa=' + ('true' if self.pdfa else 'false')])
        if len(yaml_to_use) > 0:
            subprocess_arguments.extend(yaml_to_use)
        if self.template_file is not None:
            subprocess_arguments.extend(['--template=%s' % self.template_file])
        if self.reference_file is not None:
            if PANDOC_OLD:
                subprocess_arguments.extend(['--reference-docx=%s' % self.reference_file])
            else:
                subprocess_arguments.extend(['--reference-doc=%s' % self.reference_file])
        subprocess_arguments.extend(['-s', '-o', temp_outfile.name])
        subprocess_arguments.extend([temp_file.name])
        subprocess_arguments.extend(self.arguments)
        #logmessage("Arguments are " + str(subprocess_arguments) + " and directory is " + tempfile.gettempdir())
        try:
            msg = subprocess.check_output(subprocess_arguments, cwd=tempfile.gettempdir(), stderr=subprocess.STDOUT).decode('utf-8', 'ignore')
        except subprocess.CalledProcessError as err:
            raise Exception("Failed to assemble file: " + err.output.decode())
        if msg:
            self.pandoc_message = msg
        os.remove(temp_file.name)
        if os.path.exists(temp_outfile.name):
            if self.output_format in ('rtf', 'rtf to docx'):
                with open(temp_outfile.name, encoding='utf-8') as the_file:
                    file_contents = the_file.read()
                # with open('/tmp/asdf.rtf', 'w') as deb_file:
                #     deb_file.write(file_contents)
                file_contents = docassemble.base.filter.rtf_filter(file_contents, metadata=metadata_as_dict, styles=get_rtf_styles(self.template_file), question=question)
                with open(temp_outfile.name, "wb") as the_file:
                    the_file.write(bytearray(file_contents, encoding='utf-8'))
                if self.output_format == 'rtf to docx':
                    docx_outfile = tempfile.NamedTemporaryFile(prefix="datemp", mode="wb", suffix=".docx", delete=False)
                    success = rtf_to_docx(temp_outfile.name, docx_outfile.name)
                    if not success:
                        raise Exception("Could not convert RTF to DOCX.")
                    temp_outfile = docx_outfile
            if self.output_filename is not None:
                shutil.copyfile(temp_outfile.name, self.output_filename)
            else:
                self.output_filename = temp_outfile.name
            self.output_content = None
            if self.output_format == 'pdf' and self.password:
                pdf_encrypt(self.output_filename, self.password)
        else:
            raise IOError("Failed creating file: %s" % output_filename)
        return
    def convert(self, question):
        latex_conversion_directory = os.path.join(tempfile.gettempdir(), 'conv')
        if not os.path.isdir(latex_conversion_directory):
            os.makedirs(latex_conversion_directory)
        if not os.path.isdir(latex_conversion_directory):
            raise Exception("Could not create latex conversion directory")
        if self.output_format in ("pdf", "tex", "rtf", "rtf to docx", "epub", "docx"):
            self.convert_to_file(question)
        else:
            subprocess_arguments = [PANDOC_PATH, PANDOC_ENGINE]
            if PANDOC_OLD:
                input_format = self.input_format
                subprocess_arguments.append("--smart")
            else:
                if self.input_format == 'markdown':
                    input_format = "markdown+smart"
            subprocess_arguments.extend(['-M', 'latextmpdir=' + os.path.join('.', 'conv'), '--from=%s' % input_format, '--to=%s' % self.output_format])
            if self.output_format == 'html':
                subprocess_arguments.append('--ascii')
            subprocess_arguments.extend(self.arguments)
            #logmessage("Arguments are " + str(subprocess_arguments))
            p = subprocess.Popen(
                subprocess_arguments,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                cwd=tempfile.gettempdir()
            )
            self.output_filename = None
            #logmessage("input content is a " + self.input_content.__class__.__name__)
            #with open('/tmp/moocow1', 'wb') as fp:
            #    fp.write(bytearray(self.input_content, encoding='utf-8'))
            self.output_content = p.communicate(bytearray(self.input_content, encoding='utf-8'))[0]
            #with open('/tmp/moocow2', 'wb') as fp:
            #    fp.write(self.output_content)
            self.output_content = self.output_content.decode()
        return

def word_to_pdf(in_file, in_format, out_file, pdfa=False, password=None, update_refs=False, tagged=False):
    tempdir = tempfile.mkdtemp()
    from_file = os.path.join(tempdir, "file." + in_format)
    to_file = os.path.join(tempdir, "file.pdf")
    shutil.copyfile(in_file, from_file)
    tries = 0
    if pdfa:
        method = 'pdfa'
    elif tagged:
        method = 'tagged'
    else:
        method = 'default'
    while tries < 5:
        use_libreoffice = True
        if update_refs:
            if daconfig.get('convertapi secret', None) is not None:
                update_references(from_file)
                try:
                    convertapi_to_pdf(from_file, to_file)
                    result = 0
                except:
                    logmessage("Call to convertapi failed")
                    result = 1
                use_libreoffice = False
            else:
                subprocess_arguments = [LIBREOFFICE_PATH, '--headless', '--invisible', 'macro:///Standard.Module1.ConvertToPdf(' + from_file + ',' + to_file + ',True,' + method + ')']
        elif daconfig.get('convertapi secret', None) is not None:
            try:
                convertapi_to_pdf(from_file, to_file)
                result = 0
            except:
                logmessage("Call to convertapi failed")
                result = 1
            use_libreoffice = False
        else:
            if method == 'default':
                subprocess_arguments = [LIBREOFFICE_PATH, '--headless', '--convert-to', 'pdf', from_file]
            else:
                subprocess_arguments = [LIBREOFFICE_PATH, '--headless', '--invisible', 'macro:///Standard.Module1.ConvertToPdf(' + from_file + ',' + to_file + ',False,' + method + ')']
        if use_libreoffice:
            initialize_libreoffice()
            #logmessage("Trying libreoffice with " + repr(subprocess_arguments))
            p = subprocess.Popen(subprocess_arguments, cwd=tempdir)
            result = p.wait()
        if os.path.isfile(to_file):
            break
        result = 1
        tries += 1
        time.sleep(2 + tries*random.random())
        if use_libreoffice:
            logmessage("Retrying libreoffice with " + repr(subprocess_arguments))
        else:
            logmessage("Retrying convertapi")
        continue
    if result == 0:
        if password:
            pdf_encrypt(to_file, password)
        shutil.copyfile(to_file, out_file)
    if tempdir is not None:
        shutil.rmtree(tempdir)
    if result != 0:
        return False
    return True

def rtf_to_docx(in_file, out_file):
    initialize_libreoffice()
    tempdir = tempfile.mkdtemp()
    from_file = os.path.join(tempdir, "file.rtf")
    to_file = os.path.join(tempdir, "file.docx")
    shutil.copyfile(in_file, from_file)
    subprocess_arguments = [LIBREOFFICE_PATH, '--headless', '--convert-to', 'docx', from_file]
    p = subprocess.Popen(subprocess_arguments, cwd=tempdir)
    result = p.wait()
    if not os.path.isfile(to_file):
        result = 1
    if result == 0:
        shutil.copyfile(to_file, out_file)
    if tempdir is not None:
        shutil.rmtree(tempdir)
    if result != 0:
        return False
    return True

def word_to_markdown(in_file, in_format):
    initialize_libreoffice()
    temp_file = tempfile.NamedTemporaryFile(mode="wb", suffix=".md")
    if in_format not in ['docx', 'odt']:
        tempdir = tempfile.mkdtemp()
        from_file = os.path.join(tempdir, "file." + in_format)
        to_file = os.path.join(tempdir, "file.docx")
        shutil.copyfile(in_file, from_file)
        subprocess_arguments = [LIBREOFFICE_PATH, '--headless', '--convert-to', 'docx', from_file]
        p = subprocess.Popen(subprocess_arguments, cwd=tempdir)
        result = p.wait()
        if result != 0:
            return None
        in_file_to_use = to_file
        in_format_to_use = 'docx'
    else:
        in_file_to_use = in_file
        in_format_to_use = in_format
        tempdir = None
    subprocess_arguments = [PANDOC_PATH, PANDOC_ENGINE]
    if PANDOC_OLD:
        subprocess_arguments.append("--smart")
    else:
        if in_format_to_use == 'markdown':
            in_format_to_use = "markdown+smart"
    subprocess_arguments.extend(['--from=%s' % str(in_format_to_use), '--to=markdown', str(in_file_to_use), '-o', str(temp_file.name)])
    result = subprocess.call(subprocess_arguments)
    if tempdir is not None:
        shutil.rmtree(tempdir)
    if result == 0:
        final_file = tempfile.NamedTemporaryFile(mode="wb", suffix=".md")
        with open(temp_file.name, 'rU', encoding='utf-8') as the_file:
            file_contents = the_file.read()
        file_contents = re.sub(r'\\([\$\[\]])', lambda x: x.group(1), file_contents)
        with open(final_file.name, "w", encoding='utf-8') as the_file:
            the_file.write(file_contents)
        return final_file
    else:
        return None
    
def get_rtf_styles(filename):
    file_contents = ''
    styles = dict()
    with open(filename) as the_file:
        file_contents = the_file.read()
        for (style_string, style_number, heading_number) in re.findall(style_find, file_contents):
            style_string = re.sub(r'\s+', ' ', style_string, flags=re.DOTALL)
            #logmessage("heading " + str(heading_number) + " is style " + str(style_number))
            styles[heading_number] = style_string
    return styles
    
def update_references(filename):
    initialize_libreoffice()
    subprocess_arguments = [LIBREOFFICE_PATH, '--headless', '--invisible', 'macro:///Standard.Module1.PysIndexer(' + filename + ')']
    p = subprocess.Popen(subprocess_arguments, cwd=tempfile.gettempdir())
    result = p.wait()
    if result != 0:
        return False
    return True

def initialize_libreoffice():
    if LIBREOFFICE_INITIALIZED:
        return
    global LIBREOFFICE_INITIALIZED
    LIBREOFFICE_INITIALIZED = True
    if not os.path.isfile(LIBREOFFICE_MACRO_PATH):
        logmessage("No LibreOffice macro path exists")
        temp_file = tempfile.NamedTemporaryFile(prefix="datemp", mode="wb", suffix=".pdf")
        word_file = docassemble.base.functions.package_template_filename('docassemble.demo:data/templates/template_test.docx')
        word_to_pdf(word_file, 'docx', temp_file.name, pdfa=False, password=None)
        del temp_file
        del word_file
    try:
        assert os.path.isdir(os.path.dirname(LIBREOFFICE_MACRO_PATH))
        orig_path = docassemble.base.functions.package_template_filename('docassemble.base:data/macros/Module1.xba')
        logmessage("Copying LibreOffice macro from " + orig_path)
        shutil.copyfile(orig_path, LIBREOFFICE_MACRO_PATH)
    except:
        logmessage("Could not copy LibreOffice macro into place")

def concatenate_files(path_list, pdfa=False, password=None):
    pdf_file = tempfile.NamedTemporaryFile(prefix="datemp", mode="wb", suffix=".pdf", delete=False)
    subprocess_arguments = [PDFTK_PATH]
    new_path_list = list()
    for path in path_list:
        mimetype, encoding = mimetypes.guess_type(path)
        if mimetype.startswith('image'):
            new_pdf_file = tempfile.NamedTemporaryFile(prefix="datemp", mode="wb", suffix=".pdf", delete=False)
            args = ["convert", path, new_pdf_file.name]
            result = call(args)
            if result != 0:
                logmessage("failed to convert image to PDF: " + " ".join(args))
                continue
            new_path_list.append(new_pdf_file.name)
        elif mimetype in ('application/rtf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword', 'application/vnd.oasis.opendocument.text'):
            new_pdf_file = tempfile.NamedTemporaryFile(prefix="datemp", mode="wb", suffix=".pdf", delete=False)
            if mimetype == 'application/rtf':
                ext = 'rtf'
            elif mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                ext = 'docx'
            elif mimetype == 'application/msword':
                ext = 'doc'
            elif mimetype == 'application/vnd.oasis.opendocument.text':
                ext = 'odt'
            word_to_pdf(path, ext, new_pdf_file.name, pdfa=False)
            new_path_list.append(new_pdf_file.name)
        elif mimetype == 'application/pdf':
            new_path_list.append(path)
    if len(new_path_list) == 0:
        raise DAError("concatenate_files: no valid files to concatenate")
    subprocess_arguments.extend(new_path_list)
    subprocess_arguments.extend(['cat', 'output', pdf_file.name])
    #logmessage("Arguments are " + str(subprocess_arguments))
    result = call(subprocess_arguments)
    if result != 0:
        logmessage("Failed to concatenate PDF files")
        raise DAError("Call to pdftk failed for concatenation where arguments were " + " ".join(subprocess_arguments))
    if pdfa:
        pdf_to_pdfa(pdf_file.name)
    replicate_js_and_calculations(new_path_list[0], pdf_file.name, password)
    return pdf_file.name
