// C04 M03 清江一线 — SOFT-HOLD Neutral Prototype v1.3
// GATE-2 RELATIONAL MOCKUP ONLY. NOT PRODUCT DIMENSION / MATERIAL / MECHANISM AUTHORITY.
// Prototype scale is an explicit test assumption for hand/carry visualization.

$fn = 28;

prototype_length = 240; // mm — MOCKUP ASSUMPTION ONLY
rod_d = 10;             // mm — MOCKUP ASSUMPTION ONLY
cap_d = 13;             // mm — MOCKUP ASSUMPTION ONLY

module capsule_between(a,b,d=rod_d){
  hull(){
    translate(a) sphere(d=d);
    translate(b) sphere(d=d);
  }
}

module line_from(points,d=rod_d){
  for(i=[0:len(points)-2]) capsule_between(points[i], points[i+1], d);
  translate(points[0]) sphere(d=cap_d);
  translate(points[len(points)-1]) sphere(d=cap_d);
}

module carry_state(){
  // low-profile folded relation; does NOT imply a bracelet/necklace loop.
  pts=[[-100,0,0],[-62,18,0],[-24,-10,0],[18,12,0],[58,-12,0],[100,5,0]];
  line_from(pts);
}

module reform_state(){
  // coarse two-hand S-like relation; not a route silhouette.
  pts=[[-108,-8,0],[-76,28,0],[-34,38,0],[5,8,0],[42,-30,0],[78,-14,0],[108,26,0]];
  line_from(pts);
}

module revisit_state(){
  // temporarily held personal trace: asymmetric and intentionally non-cartographic.
  pts=[[-108,12,0],[-78,-18,0],[-40,-26,0],[-4,4,0],[35,26,0],[72,18,0],[108,-14,0]];
  line_from(pts);
}

module scale_bar(){
  // visual-only mockup scale marker, not final product specification.
  translate([-120,-62,0]) cube([50,2,2]);
  translate([-120,-67,0]) linear_extrude(height=1) text("50 mm MOCKUP", size=6);
}

state = is_undef(state) ? "reform" : state;

color([0.55,0.58,0.56]) {
  if(state=="carry") carry_state();
  else if(state=="revisit") revisit_state();
  else reform_state();
}
scale_bar();
