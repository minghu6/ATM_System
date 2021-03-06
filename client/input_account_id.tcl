#############################################################################
# Generated by PAGE version 4.7
# in conjunction with Tcl version 8.6
#    Mar 29, 2016 10:56:35 AM


set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #d9d9d9
set vTcl(active_fg) #111111
#############################################################################
#################################
#LIBRARY PROCEDURES
#


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top36
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# USER DEFINED PROCEDURES
#

#################################
# GENERATED GUI PROCEDURES
#

proc vTclWindow.top36 {base} {
    if {$base == ""} {
        set base .top36
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background {#d9d9d9} 
    wm focusmodel $top passive
    wm geometry $top 433x113+1231+238
    update
    # set in toplevel.wgt.
    global vTcl
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1916 1053
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "Input Transfer Account ID"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    entry $top.ent37 \
        -background white -disabledforeground {#a3a3a3} -font font11 \
        -foreground {#000000} -insertbackground black 
    vTcl:DefineAlias "$top.ent37" "btn_transfer_to_id" vTcl:WidgetProc "Toplevel1" 1
    ttk::style configure TButton -background #d9d9d9
    ttk::style configure TButton -foreground #000000
    ttk::style configure TButton -font TkDefaultFont
    ttk::button $top.tBu40 \
        -takefocus {} -text OK 
    vTcl:DefineAlias "$top.tBu40" "btn_ok" vTcl:WidgetProc "Toplevel1" 1
    ttk::style configure TButton -background #d9d9d9
    ttk::style configure TButton -foreground #000000
    ttk::style configure TButton -font TkDefaultFont
    ttk::button $top.tBu41 \
        -takefocus {} -text Cancel 
    vTcl:DefineAlias "$top.tBu41" "btn_cancle" vTcl:WidgetProc "Toplevel1" 1
    ttk::label $top.tLa42 \
        -background {#d9d9d9} -foreground {#000000} -relief flat \
        -text TransferID 
    vTcl:DefineAlias "$top.tLa42" "TLabel1" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.ent37 \
        -in $top -x 80 -y 30 -width 334 -height 27 -anchor nw \
        -bordermode ignore 
    place $top.tBu40 \
        -in $top -x 60 -y 70 -width 97 -height 37 -anchor nw \
        -bordermode ignore 
    place $top.tBu41 \
        -in $top -x 320 -y 70 -width 97 -height 37 -anchor nw \
        -bordermode ignore 
    place $top.tLa42 \
        -in $top -x 0 -y 30 -width 79 -height 21 -anchor nw \
        -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

#############################################################################
## Binding tag:  _TopLevel

bind "_TopLevel" <<Create>> {
    if {![info exists _topcount]} {set _topcount 0}; incr _topcount
}
bind "_TopLevel" <<DeleteWindow>> {
    if {[set ::%W::_modal]} {
                vTcl:Toplevel:WidgetProc %W endmodal
            } else {
                destroy %W; if {$_topcount == 0} {exit}
            }
}
bind "_TopLevel" <Destroy> {
    if {[winfo toplevel %W] == "%W"} {incr _topcount -1}
}

Window show .
Window show .top36

