#@+leo-ver=5-thin
#@+node:peckj.20150428142633.1: * @file python_terminal.py
#@@language python
#@@tabwidth -4

# this code from http://stackoverflow.com/questions/12431555/enabling-code-completion-in-an-embedded-python-interpreter
# with modifications from Jake Peck

# to do:
  # styling

#@+<< docstring >>
#@+node:peckj.20150428142633.2: ** << docstring >>
'''Provides an interactive python terminal in the log pane.

**Warning**: Use at your own risk.
Numerous significant problems have been reported, including segfaults.


By Jacob M. Peck

Usage
=====
Enabling this plugin will add a new tab to the Log pane, labeled "Python Console".  This is a fully interactive
python command shell, with access to `g`, `c`, and `p` included!

Features:
- Includes support for g, c, and p
- Each outline tab has a separate python console, with a separate namespace (aside from g, of course)
- Extremely primitive tab-completion
- Command history (use !hist to list, and !hist(n) to recall the n'th entry)
- !clear to clear the console

Caveats:

Stdout and stderr are proprely redirected to the interactive console pane while
it has focus, but proprely reset to their previous values when focus is lost. If
code executed inside the interactive console pane needs to output to the
command-line stdout/stderr, please use sys.__stdout__ and sys.__stderr__. - Just
as with scripts, if you do something dangerous, you're on your own

This code is largely lifted from
http://stackoverflow.com/questions/12431555/
enabling-code-completion-in-an-embedded-python-interpreter,
with some modifications made for Leo embedding.
'''
#@-<< docstring >>
#@+<< imports >>
#@+node:peckj.20150428142729.2: ** << imports >>
import leo.core.leoGlobals as g

# import os
import re
import sys
import code
from rlcompleter import Completer

from leo.core.leoQt import QtWidgets,QtCore
#@-<< imports >>

#@+others
#@+node:peckj.20150428142729.3: ** class MyInterpreter
if QtWidgets:
    
    class MyInterpreter(QtWidgets.QWidget):
    
        def __init__(self, parent, c):
            super(MyInterpreter, self).__init__(parent)
            hBox = QtWidgets.QHBoxLayout()
            self.setLayout(hBox)
            self.textEdit = PyInterp(self, c)
            # this is how you pass in locals to the interpreter
            self.textEdit.initInterpreter(locals())
            hBox.addWidget(self.textEdit)
            hBox.setContentsMargins(0,0,0,0)
            hBox.setSpacing(0)
#@+node:peckj.20150428142729.5: ** class PyInterp (QTextEdit)
if QtWidgets:
    
    class PyInterp(QtWidgets.QTextEdit):
        #@+others
        #@+node:peckj.20150428142729.6: *3* class InteractiveInterpreter (code.InteractiveInterpreter)
        class InteractiveInterpreter(code.InteractiveInterpreter):
            #@+others
            #@+node:peckj.20150428142729.7: *4* InteractiveInterpreter.__init__
            def __init__(self, locals, c):
                '''Ctor for InteractiveInterpreter class.'''
                self.c = c
                # inject g, c, p
                loc = locals
                loc['c'] = self.c
                loc['g'] = g
                loc['p'] = self.c.p

                code.InteractiveInterpreter.__init__(self, loc)
            #@+node:peckj.20150428142729.8: *4* InteractiveInterpreter.runIt
            def runIt(self, command):

                code.InteractiveInterpreter.runsource(self, command)
            #@-others
        #@+node:peckj.20150428142729.9: *3* PyInterp.__init__
        def __init__(self, parent, c):
            super(PyInterp, self).__init__(parent)
            #
            # this widget swallows stdout + stderr while focused,
            # but resets them upon losing focus
            if not g.user_dict.get('old_stdout', None):
                g.user_dict['old_stdout'] = sys.stdout
            if not g.user_dict.get('old_stderr', None):
                g.user_dict['old_stderr'] = sys.stderr
            #
            # init ivars.
            self.indent = 0
            self.refreshMarker = False # to change back to >>> from ...
            self.multiLine = False # code spans more than one line
            ### self.command        = ''    # command to be ran
            self.printBanner() # print sys info
            self.insert_marker() # make the >>> or ... marker
            self.history = [] # list of commands entered
            self.historyIndex = -1
            self.interpreterLocals = {}
            self.c = c
            #
            # initilize interpreter with self locals
            self.initInterpreter(locals())
            #
            # update p when new node selected
            g.registerHandler('select2', self.select2_hook)
        #@+node:peckj.20150428142729.10: *3* PyInterp.select2_hook
        def select2_hook(self, tag, keywords):
            self.interpreter.runIt('p = c.p')
        #@+node:peckj.20150428142729.11: *3* PyInterp.printBanner
        def printBanner(self):
            #self.write(sys.version)
            #self.write(' on ' + sys.platform + '\n')
            #self.write('PyQt4 ' + PYQT_VERSION_STR + '\n')
            banner = [
                'Type !hist for a history view and !hist(n) history index recall\n',
                'Type !clear to clear this pane\n'
            ]
            for msg in banner:
                self.write(msg)
        #@+node:peckj.20150428142729.12: *3* PyInterp.insert_marker
        def insert_marker(self):
            
            line = '... ' if self.multiLine else '>>> '
            self.insertPlainText(line + ' '*self.indent)
        #@+node:peckj.20150428142729.13: *3* PyInterp.initInterpreter
        def initInterpreter(self, interpreterLocals=None):
            if interpreterLocals:
                # when we pass in locals, we don't want it to be named "self"
                # so we rename it with the name of the class that did the passing
                # and reinsert the locals back into the interpreter dictionary
                selfName = interpreterLocals['self'].__class__.__name__
                interpreterLocalVars = interpreterLocals.pop('self')
                self.interpreterLocals[selfName] = interpreterLocalVars
            else:
                self.interpreterLocals = interpreterLocals
            self.interpreter = self.InteractiveInterpreter(self.interpreterLocals, self.c)
        #@+node:peckj.20150428142729.14: *3* PyInterp.updateInterpreterLocals
        def updateInterpreterLocals(self, newLocals):
            className = newLocals.__class__.__name__
            self.interpreterLocals[className] = newLocals
        #@+node:peckj.20150428142729.15: *3* PyInterp.write
        def write(self, line):
            self.insertPlainText(line)
            self.ensureCursorVisible()
        #@+node:peckj.20150428142729.16: *3* PyInterp.clearCurrentBlock
        def clearCurrentBlock(self):
            # block being current row
            length = len(self.document().lastBlock().text()[4:])
            if length == 0:
                return None
            else:
                # should have a better way of doing this but I can't find it.
                # [self.textCursor().deletePreviousChar() for x in xrange(length)]
                for x in range(length):
                    self.textCursor().deletePreviousChar()
            return True
        #@+node:peckj.20150428142729.17: *3* PyInterp.recallHistory
        def recallHistory(self):
            # used when using the arrow keys to scroll through history
            self.clearCurrentBlock()
            if self.historyIndex != -1:
                self.insertPlainText(self.history[self.historyIndex])
            return True
        #@+node:peckj.20150428142729.18: *3* PyInterp.customCommands
        def customCommands(self, command):

            # pylint: disable=anomalous-backslash-in-string

            if command == '!hist': # display history
                self.append('') # move down one line
                # vars that are in the command are prefixed with ____CC and deleted
                # once the command is done so they don't show up in dir()
                backup = self.interpreterLocals.copy()
                history = self.history[:]
                history.reverse()
                for i, x in enumerate(history):
                    iSize = len(str(i))
                    delta = len(str(len(history))) - iSize
                    line = line  = ' ' * delta + '%i: %s' % (i, x) + '\n'
                    self.write(line)
                self.updateInterpreterLocals(backup)
                self.insert_marker()
                return True

            if re.match('!hist\(\d+\)', command): # recall command from history
                backup = self.interpreterLocals.copy()
                history = self.history[:]
                history.reverse()
                index = int(command[6:-1])
                self.clearCurrentBlock()
                command = history[index]
                if command[-1] == ':':
                    self.multiLine = True
                self.write(command)
                self.updateInterpreterLocals(backup)
                return True

            if re.match('(quit|exit)\(\)', command): # prevent quitting!
                self.append('')
                self.write('Cannot quit() from an embedded console.\n')
                self.insert_marker()
                return True

            if re.match('!clear', command): # clear the screen
                self.clear()
                self.insert_marker()
                return True

            return False
        #@+node:peckj.20150428142729.19: *3* PyInterp.keyPressEvent & helper
        def keyPressEvent(self, event):
            qt = QtCore.Qt
            if event.key() == qt.Key_Tab:
                line = str(self.document().lastBlock().text())[4:]
                completer = Completer(self.interpreter.locals)
                suggestion = completer.complete(line, 0)
                if suggestion is not None:
                    self.insertPlainText(suggestion[len(line):])
                return None

            if event.key() == qt.Key_Down:
                if self.historyIndex == len(self.history):
                    self.historyIndex -= 1
                try:
                    if self.historyIndex > -1:
                        self.historyIndex -= 1
                        self.recallHistory()
                    else:
                        self.clearCurrentBlock()
                except Exception:
                    pass
                return None

            if event.key() == qt.Key_Up:
                try:
                    if len(self.history) - 1 > self.historyIndex:
                        self.historyIndex += 1
                        self.recallHistory()
                    else:
                        self.historyIndex = len(self.history)
                except Exception:
                    pass
                return None

            if event.key() == qt.Key_Home:
                # set cursor to position 4 in current block. 4 because that's where
                # the marker stops
                blockLength = len(self.document().lastBlock().text()[4:])
                lineLength  = len(self.document().toPlainText())
                position = lineLength - blockLength
                textCursor  = self.textCursor()
                textCursor.setPosition(position)
                self.setTextCursor(textCursor)
                return None

            if event.key() in [qt.Key_Left, qt.Key_Backspace]:
                # don't allow deletion of marker
                if self.textCursor().positionInBlock() == 4:
                    return None

            if event.key() in [qt.Key_Return, qt.Key_Enter]:
                self.doEnter(event)
                return None
                
            # allow all other key events
            super(PyInterp, self).keyPressEvent(event)
        #@+node:ekr.20180307132016.1: *4* PyInterp.doEnter
        def doEnter(self, event):
            '''Handle the <return> key.'''
            #
            # Set cursor to end of line to avoid line splitting
            textCursor = self.textCursor()
            position   = len(self.document().toPlainText())
            textCursor.setPosition(position)
            self.setTextCursor(textCursor)
            lines = []
            block = self.document().lastBlock()
            #
            # Scan backward, looking for lines.
            pasteFlag = False
            while block:
                line = g.toUnicode(block.text())
                line = line.replace('\t',' '*4)
                block = block.previous()
                if line.startswith('>>> '):
                    lines.insert(0, line[4:].rstrip())
                    break
                elif line.startswith('... '):
                    lines.insert(0, line[4:].rstrip())
                else:
                    lines.insert(0, line.rstrip())
                    pasteFlag = True
            # Enter continuation mode for pasted lines.
            if pasteFlag and lines and lines[-1].strip():
                self.multiLine = True
            #
            # Always end the input.
            self.append('')
            #
            # Handle special lines.
            last_line = lines and lines[-1]
            if self.customCommands(last_line):
                return
            # Handle the history and indent.
            if last_line.strip():
                self.history.insert(0, last_line.rstrip())
                self.indent = len(last_line) - len(last_line.lstrip())
                if last_line.rstrip().endswith(':'):
                    self.indent += 4
            #
            # Just return if the last line if it is a non-blank continued line.
            if len(lines) > 1 and last_line.strip():
                self.insert_marker()
                return
            #
            # Clean the lines.
            lines = [z for z in lines if z.strip()]
            #
            # Just add the marker if we are done.
            if not lines:
                self.insert_marker()
                return
            the_code = self.compile_lines(lines)
            if the_code is None:
                # Continuation mode.
                self.multiLine = True
                self.insert_marker()
                return
            #
            # End continuation mode.
            self.multiLine = False
            self.indent = 0
            if the_code != 'error':
                self.run_code(the_code)
            self.insert_marker()
        #@+node:ekr.20180525110448.1: *5* PyInterp.compile_lines
        def compile_lines(self, lines):
            '''Carefully call code.compile_command and return the result.'''
            #
            # The compile command saves a lot of guessing...
            # https://docs.python.org/2/library/code.html#code.compile_command
            try:
                interp = self.interpreter
                source = '\n'.join(lines).rstrip() + '\n'
                return code.compile_command(source)
            except SyntaxError:
                # When pasting, try to separate lines with semicolons.
                if len(lines) > 1:
                    try:
                        source = ';'.join(lines).rstrip() + '\n'
                        return code.compile_command(source)
                    except SyntaxError:
                        interp.showsyntaxerror()
                    except Exception:
                        interp.showtraceback()
                else:
                    interp.showsyntaxerror()
            except Exception:
                interp.showtraceback()
            #
            # End the previous editing if there is any error.
            self.multiLine = False
            return 'error'
        #@+node:ekr.20180525110907.1: *5* PyInterp.run_code
        def run_code(self, the_code):
            
            interp = self.interpreter
            try:
                interp.runcode(the_code)
            except SyntaxError:
                interp.showsyntaxerror()
            except Exception:
                interp.showtraceback()
        #@+node:peckj.20150428142729.20: *3* PyInterp.focusInEvent
        def focusInEvent(self, event=None):
            # set stdout+stderr properly
            QtWidgets.QTextEdit.focusInEvent(self,event)
            sys.stdout = self
            sys.stderr = self
            self.ensureCursorVisible()
        #@+node:peckj.20150428142729.21: *3* PyInterp.focusOutEvent
        def focusOutEvent(self, event):
            # set stdout+stderr properly
            QtWidgets.QTextEdit.focusOutEvent(self,event)
            sys.stdout = g.user_dict['old_stdout']
            sys.stderr = g.user_dict['old_stderr']
        #@-others









#@+node:peckj.20150428142633.4: ** init
def init ():
    '''Return True if the plugin has loaded successfully.'''
    if g.app.gui is None:
        g.app.createQtGui(__file__)
    ok = g.app.gui.guiName().startswith('qt')
    if ok:
        # g.registerHandler(('new','open2'),onCreate)
        g.registerHandler('after-create-leo-frame',onCreate)
            # Fail: g.app.log does not exist.
        g.plugin_signon(__name__)
    else:
        g.es('Plugin %s not loaded.' % __name__, color='red')
    return ok
#@+node:peckj.20150428142633.5: ** onCreate
def onCreate (tag, keys):
    '''python_terminal.py onCreate handler.'''
    c = keys.get('c')
    if c:
        win = MyInterpreter(None,c)
        c.frame.log.createTab('Python Console',widget=win)
#@-others


#@-leo
