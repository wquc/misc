# trace vdelete vmd_pick_atom w query_atom

set label_ids {}

proc clear_label {} {
    draw delete all
}

proc undo_label {} {
    global  label_ids
    set last_labeled [lindex $label_ids end]
    draw delete $last_labeled
    set label_ids [lreplace $label_ids end end]
}

proc query_atom { args } {
    draw color black
    #          ^^^^^ Modify draw color here
    global vmd_pick_atom vmd_pick_mol
    global last_labeled label_ids

    set sele [atomselect $vmd_pick_mol "same residue as index $vmd_pick_atom"]
    set name [$sele get resname]
    set name [lsort -unique $name]

    set coor [lindex [$sele get {x y z} ] 0]
    set x [lindex $coor 0]
    set y [lindex $coor 1]
    set z [lindex $coor 2]
    
    set last_labeled [draw text "$x $y $z" $name size 1 thickness 2]
    lappend label_ids $last_labeled
}

trace variable vmd_pick_atom w query_atom 
user add key w { mouse mode pick }
user add key q { clear_label }
user add key z { undo_label }
