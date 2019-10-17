proc enabletrace {} {
    global vmd_frame
    trace variable vmd_frame([molinfo top]) w saltbridge
}

proc disabletrace {} {	 
    global vmd_frame
    trace vdelete vmd_frame([molinfo top]) w saltbridge
}

# when the frame changes, trace calls this function
proc saltbridge {name element op} {
    # Salt bridge color and material
    draw delete all
    draw color purple
    draw material Goodsell
    # Define salt bridge with direction: R15 -> E14
    foreach seg1 {H I J K L M N} seg2 {N H I J K L M} {
        # 1. salt bridge candidate atoms
        set sele1 [atomselect top "resid 15 and segname $seg1 and name NH1 NH2"]
        set sele2 [atomselect top "resid 14 and segname $seg2 and name OE1 OE2"]
        set com1  [measure center $sele1]
        set com2  [measure center $sele2]
        set atoms1 [$sele1 get index]
        set atoms2 [$sele2 get index]
        # 2. examine salt bridge existence
        #  2.1 build dmat of candidate atoms
        set dmat {}
        foreach id1 $atoms1 {
            foreach id2 $atoms2 {
                set dist [measure bond [list $id1 $id2]]
                lappend dmat $dist
            }
        }
        #  2.2 draw salt bridge if exist
        foreach dist $dmat {
            if {$dist < 4.0} {
                draw line $com1 $com2 width 2
                break
            }
        }
    }
}
