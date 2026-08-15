$fn=64;
// OLEANDER Practice 2026-08-15
// Exercise assumptions only; not production dimensions.
body_w=96; body_d=58; body_h=18; corner_r=10;
button_d=18; button_h=3;
variant = is_undef(variant) ? 2 : variant;
seam = variant==1 ? 0.2 : variant==2 ? 0.6 : 1.2;

module rounded_box(w,d,h,r){
  hull(){
    for(x=[-w/2+r,w/2-r]) for(y=[-d/2+r,d/2-r])
      translate([x,y,0]) cylinder(h=h,r=r);
  }
}
module top_shell(){
  difference(){
    translate([0,0,seam/2]) rounded_box(body_w,body_d,body_h/2-seam/2,corner_r);
    translate([0,0,-1]) rounded_box(body_w-4,body_d-4,body_h/2,corner_r-2);
  }
}
module bottom_shell(){
  difference(){
    translate([0,0,-body_h/2]) rounded_box(body_w,body_d,body_h/2-seam/2,corner_r);
    translate([0,0,-body_h/2-1]) rounded_box(body_w-4,body_d-4,body_h/2,corner_r-2);
  }
}
module button(){
  translate([22,0,body_h/2+button_h/2]) cylinder(h=button_h,d=button_d,center=true);
}
module display_recess(){
  translate([-18,0,body_h/2+0.4]) cube([36,28,1],center=true);
}
color([0.86,0.86,0.86]) bottom_shell();
color([0.94,0.94,0.94]) top_shell();
color([0.2,0.2,0.2]) button();
color([0.15,0.15,0.15]) display_recess();
