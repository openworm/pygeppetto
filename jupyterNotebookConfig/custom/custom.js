document.domain='gpt.org'
require.undef('geppettoWidgets');

define('geppettoWidgets', ["jupyter-js-widgets"], function(widgets) {

var geppettoJupyterWidgets = window.parent.require('components/GeppettoJupyterWidgets')

    return {
        PanelView: geppettoJupyterWidgets.PanelView,
        PanelModel: geppettoJupyterWidgets.PanelModel,
        ComponentView: geppettoJupyterWidgets.ComponentView,
        ComponentModel: geppettoJupyterWidgets.ComponentModel
    };
});

$([IPython.events]).on('notebook_loaded.Notebook', function(){
    $('#header').hide();

    IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-`', function (event) {
        if (IPython.notebook.mode == 'command') {
            $('#header').toggle();
            return false;
        }
        return true;
    });
});
