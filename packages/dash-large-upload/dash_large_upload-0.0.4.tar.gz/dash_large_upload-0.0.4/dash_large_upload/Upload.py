# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Upload(Component):
    """A Upload component.


Keyword arguments:
- maxFiles (number; optional): Maximum number of files that can be uploaded in one session
- maxFileSize (number; optional): Maximum size per file in bytes.
- chunkSize (number; optional): Size of file chunks to send to server.
- simultaneousUploads (number; optional): Number of simultaneous uploads to select
- service (string; optional): The service to send the files to
- className (string; optional): Class to add to the upload component by default
- hoveredClass (string; optional): Class to add to the upload component when it is hovered
- disabledClass (string; optional): Class to add to the upload component when it is disabled
- pausedClass (string; optional): Class to add to the upload component when it is paused
- completeClass (string; optional): Class to add to the upload component when it is complete
- uploadingClass (string; optional): Class to add to the upload component when it is uploading
- defaultStyle (dict; optional): Style attributes to add to the upload component
- activeStyle (dict; optional): Style when upload component is hovered over
- completeStyle (dict; optional): Style when upload is completed (upload finished)
- textLabel (string; optional): The string to display in the upload component
- completedMessage (string; optional): Message to display when upload completed
- fileNames (list; optional): The names of the files uploaded
- filetypes (list; optional): List of allowed file types, e.g. ['jpg', 'png']
- startButton (boolean; optional): Whether or not to have a start button
- pauseButton (boolean; optional): Whether or not to have a pause button
- cancelButton (boolean; optional): Whether or not to have a cancel button
- disableDragAndDrop (boolean; optional): Whether or not to allow file drag and drop
- id (string; optional): User supplied id of this component"""
    @_explicitize_args
    def __init__(self, maxFiles=Component.UNDEFINED, maxFileSize=Component.UNDEFINED, chunkSize=Component.UNDEFINED, simultaneousUploads=Component.UNDEFINED, service=Component.UNDEFINED, className=Component.UNDEFINED, hoveredClass=Component.UNDEFINED, disabledClass=Component.UNDEFINED, pausedClass=Component.UNDEFINED, completeClass=Component.UNDEFINED, uploadingClass=Component.UNDEFINED, defaultStyle=Component.UNDEFINED, activeStyle=Component.UNDEFINED, completeStyle=Component.UNDEFINED, textLabel=Component.UNDEFINED, completedMessage=Component.UNDEFINED, fileNames=Component.UNDEFINED, filetypes=Component.UNDEFINED, startButton=Component.UNDEFINED, pauseButton=Component.UNDEFINED, cancelButton=Component.UNDEFINED, disableDragAndDrop=Component.UNDEFINED, id=Component.UNDEFINED, simultaneuosUploads=Component.UNDEFINED, **kwargs):
        self._prop_names = ['maxFiles', 'maxFileSize', 'chunkSize', 'simultaneousUploads', 'service', 'className', 'hoveredClass', 'disabledClass', 'pausedClass', 'completeClass', 'uploadingClass', 'defaultStyle', 'activeStyle', 'completeStyle', 'textLabel', 'completedMessage', 'fileNames', 'filetypes', 'startButton', 'pauseButton', 'cancelButton', 'disableDragAndDrop', 'id']
        self._type = 'Upload'
        self._namespace = 'dash_large_upload'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['maxFiles', 'maxFileSize', 'chunkSize', 'simultaneousUploads', 'service', 'className', 'hoveredClass', 'disabledClass', 'pausedClass', 'completeClass', 'uploadingClass', 'defaultStyle', 'activeStyle', 'completeStyle', 'textLabel', 'completedMessage', 'fileNames', 'filetypes', 'startButton', 'pauseButton', 'cancelButton', 'disableDragAndDrop', 'id']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Upload, self).__init__(**args)
