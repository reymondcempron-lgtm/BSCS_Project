import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ─── 3D modern tropical house ────────────────────────────────────────────
// HOW TO EDIT: Dimensions, materials, and decorative elements are below.
// The camera uses OrbitControls: drag to rotate, wheel to zoom, right-drag to pan.

const viewport = document.getElementById('viewport');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, innerWidth / innerHeight, 0.1, 170);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(viewport.clientWidth, viewport.clientHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.37;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.domElement.setAttribute('aria-label', 'Modern tropical house, rotate with the mouse');
viewport.prepend(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.enableZoom = true;
controls.enablePan = true;
controls.minDistance = 8;
controls.maxDistance = 45;
controls.minPolarAngle = 0.07;
controls.maxPolarAngle = Math.PI / 2 - 0.05;
const target = new THREE.Vector3(0, 3.20, 0.6);
const poolTarget = new THREE.Vector3(-.65, 1.65, -7.75);
const cameraPositions = {
  angle: [12.8, 8.1, 18.8],
  front: [0.3, 6.0, 21.0],
  side: [22.0, 7.7, 2.1],
  top: [0.05, 27.0, 2.2],
  back: [12.5, 8.4, -20.5],
  pool: [-1.5, 5.2, -16.9],
};

const mat = (color, opts={}) => new THREE.MeshStandardMaterial({color,roughness:0.85,metalness:0,...opts});
const cream = mat('#e9e5d9');
const white = mat('#fffaf0');
const stucco = mat('#eee9df');
const stone = mat('#b7aca0', {roughness:0.95});
const concrete = mat('#c5beb3', {roughness:0.93});
const charcoal = mat('#272d30', {metalness:0.52,roughness:0.46});
const black = mat('#111b20', {metalness:0.63,roughness:0.27});
const walnut = mat('#704731');
const teak = mat('#9b653e');
const paleWood = mat('#b77b4b');
const soil = mat('#292e28');
const leaf1 = mat('#2d6339', {side:THREE.DoubleSide});
const leaf2 = mat('#4f7d43', {side:THREE.DoubleSide});
const leaf3 = mat('#245341', {side:THREE.DoubleSide});
const grass = mat('#416345');
const gravel = mat('#c8c6bd');
const poolTile = mat('#266e83', {roughness:.33});
const azure = new THREE.MeshPhysicalMaterial({ color:'#27b7d2', transparent:true, opacity:.85, roughness:.09, metalness:.10, clearcoat:1, clearcoatRoughness:.10, side:THREE.DoubleSide,depthWrite:false });
const ivoryTile = mat('#e7ddd0', {roughness:.73});
const polishedStone = mat('#71695f', {roughness:.46});
const blueLight = new THREE.MeshStandardMaterial({color:'#a1ffff',emissive:'#25d3e1',emissiveIntensity:1.5});
const road = mat('#3e4041', {roughness:0.55});
const glass = new THREE.MeshPhysicalMaterial({color:'#9cbcc2', transparent:true,opacity:0.38,roughness:0.08,metalness:0.3,side:THREE.DoubleSide,depthWrite:false});
const darkGlass = new THREE.MeshPhysicalMaterial({color:'#708d93',transparent:true,opacity:0.53,metalness:0.35,roughness:0.11,side:THREE.DoubleSide,depthWrite:false});
const warmLight = new THREE.MeshStandardMaterial({color:'#fff1cb',emissive:'#ffc277',emissiveIntensity:2.2});
const whiteLight = new THREE.MeshStandardMaterial({color:'#fff1dd',emissive:'#ffcc91',emissiveIntensity:1.4});
const fabric = mat('#d5cec0');
const cushion = mat('#f2e6d0');

function box(x,y,z,w,h,d, material, parent=scene, cast=true) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
  mesh.position.set(x,y,z); mesh.castShadow=cast; mesh.receiveShadow=true; parent.add(mesh); return mesh;
}
function sphere(x,y,z,r,material,parent=scene){const m=new THREE.Mesh(new THREE.SphereGeometry(r,12,9),material);m.position.set(x,y,z);m.castShadow=true;parent.add(m);return m;}
function cyl(x,y,z,r1,r2,h,material,parent=scene,radial=12){const m=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,radial),material);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
function rod(a,b,r,material,parent=scene) {const va=new THREE.Vector3(...a),vb=new THREE.Vector3(...b);const diff=vb.clone().sub(va);const mesh=new THREE.Mesh(new THREE.CylinderGeometry(r,r,diff.length(),8),material);mesh.position.copy(va).add(vb).multiplyScalar(.5);mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),diff.normalize());mesh.castShadow=true;parent.add(mesh);return mesh;}
function disk(x,y,z,r,material,parent=scene){const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,.028,24),material);m.position.set(x,y,z);parent.add(m);return m;}
function rngFactory(seed){return function(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};}
const rand = rngFactory(2026);
function ranged(a,b){return a+(b-a)*rand();}

// ─── Exterior site, road and paving ─────────────────────────────────────
box(0,-0.34,1,30,.54,34,grass);
box(0,-0.045,11.7,34,.14,9.1,road);
box(0,.03,8.30,34,.13,1.02,stone);
box(0,.12,7.86,34,.10,.12,cream);
// Road paint and wet-looking puddles (subtle, stylized).
for(let i=0;i<13;i++){
  const lane=box(-15+i*2.5,-0.015,13.8,1.12,.014,.06,mat('#9d9990',{transparent:true,opacity:.52}),scene,false);
}
for(let i=0;i<120;i++){
  const x=ranged(-15,15),z=ranged(9.05,15.7);
  sphere(x,.002,z,ranged(.015,.042),rand()>.5?stone:charcoal);
}
for (const [x,z,w,d] of [[-5.2,11,2.6,.8],[4.7,12.7,3,.9]]) {
  const m=box(x,.004,z,w,.005,d,mat('#81909a',{metalness:.2,roughness:.18,transparent:true,opacity:.22}),scene,false);
}
// Footpaths around house
box(0,.18,5.62,10.5,.26,2.4,concrete);
box(7.0,.07,.7,2.05,.09,14.0,gravel);
for(let i=0;i<9;i++)box(7.0,.17,6.7-i*1.37,1.28,.12,.67,concrete);

// ─── Architectural shell (separate wall segments for real glass openings) ──
box(0,.43,-.15,10.90,.86,10.42,stone);                    // raised foundation
box(0,.90,-.15,10.94,.14,10.47,cream);                    // floor reveal
box(0,1.02,-.12,10.36,.055,9.75,mat('#a88b6d'));        // interior warm floor
// Rear elevation: full-height real openings, not blank solid walls.
box(-4.83,2.65,-4.88,.80,3.48,.24,stucco);
box(.56,2.65,-4.88,1.67,3.48,.24,walnut);
box(4.79,2.65,-4.88,.91,3.48,.24,stucco);
box(-2.64,4.15,-4.88,3.63,.49,.24,stucco);
box(3.09,4.15,-4.88,2.54,.49,.24,stucco);
box(-2.64,1.02,-4.88,3.63,.20,.24,stone);
box(3.08,1.02,-4.88,2.54,.20,.24,stone);
box(-5.23,2.65,-.18,.28,3.48,9.55,cream);               // left wall
// Right wall is assembled around *open* windows, not painted onto a solid wall.
box(5.20,1.23,-.18,.29,.72,9.55,cream);                // bottom strip
box(5.20,5.85,-.18,.29,4.33,9.55,cream);                // solid upper wall
box(5.20,2.64,-3.80,.29,2.10,2.30,cream);              // rear edge
box(5.20,2.64,0.0,.29,2.10,1.22,cream);                // between side windows
box(5.20,2.64,3.67,.29,2.10,2.00,cream);               // front edge
// Back wall of the taller second-floor volume.
// Upper rear master bedroom with broad doors to a small sky terrace.
box(.20,5.80,-4.88,.48,3.82,.26,stucco);
box(4.65,5.80,-4.88,1.03,3.82,.26,stucco);
box(2.30,7.37,-4.88,3.40,.65,.26,stucco);
box(2.30,4.90,-4.88,3.40,.20,.26,stucco);

// Lower facade: vertical wood fin wall, large sliding glass and entry.
box(-4.70,2.65,4.78,1.05,3.48,.24,walnut);
for(let i=0;i<12;i++){
  const xx=-5.17+i*.092;
  box(xx,2.66,4.955,.041,3.28,.06,(i%4===0)?paleWood:teak);
}
box(-2.27,4.08,4.78,3.8,.58,.27,cream);                 // lintel above glazing
box(-2.24,1.075,4.78,3.75,.2,.27,cream);                // sill
box(-.18,2.6,4.79,.38,3.30,.26,cream);                  // wall beside glazing
box(2.03,4.10,4.77,4.26,.55,.28,stucco);
box(2.13,2.62,4.77,.30,3.33,.28,cream);                  // door boundary
box(.30,2.62,4.78,.40,3.34,.27,cream);
// Main wood front door
box(1.21,2.51,4.85,1.51,3.08,.11,walnut);
box(1.21,2.51,4.93,1.44,2.96,.06,paleWood);
for(let i=0;i<8;i++)box(.56+i*.19,2.51,4.975,.017,2.83,.015,teak);
rod([1.78,2.06,5.05],[1.78,2.68,5.05],.032,mat('#d0bd98',{metalness:.75,roughness:.22}));

function frontGlass(x0,x1,y0,y1,z,numberOfPanels=2){
  const cx=(x0+x1)/2,cy=(y0+y1)/2,width=x1-x0,height=y1-y0;
  box(cx,cy,z,width,height,.038,glass,scene,false);
  box(cx,y0,z+.052,width+.12,.082,.095,black);
  box(cx,y1,z+.052,width+.12,.082,.095,black);
  box(x0,cy,z+.052,.092,height+.1,.095,black);
  box(x1,cy,z+.052,.092,height+.1,.095,black);
  for(let i=1;i<numberOfPanels;i++)box(x0+width*i/numberOfPanels,cy,z+.062,.062,height,.09,charcoal);
  // Very subtle reflective highlights on the glass.
  for(let i=0;i<numberOfPanels;i++){
    box(x0+width*(i+.23)/numberOfPanels,cy,z+.076,.012,height*.82,.012,mat('#e8edf0',{transparent:true,opacity:.35}),scene,false);
  }
}
function rearGlass(x0,x1,y0,y1,z,panels=3){
  const cx=(x0+x1)*.5,cy=(y0+y1)*.5,w=x1-x0,h=y1-y0;
  box(cx,cy,z,w,h,.045,glass,scene,false);
  box(cx,y0,z-.056,w+.12,.078,.095,black);
  box(cx,y1,z-.056,w+.12,.078,.095,black);
  box(x0,cy,z-.052,.085,h+.07,.095,black);
  box(x1,cy,z-.052,.085,h+.07,.095,black);
  for(let i=1;i<panels;i++)box(x0+w*i/panels,cy,z-.062,.06,h,.09,charcoal);
}
rearGlass(-4.39,-.85,1.25,3.92,-4.92,3);
rearGlass(1.45,4.33,1.25,3.92,-4.92,3);
rearGlass(.63,3.97,4.98,7.08,-4.93,3);
// Timber privacy accent fins behind the backyard seating.
for(let i=0;i<9;i++)box(-.24+i*.087,2.65,-5.02,.031,3.06,.053,i%3===0?paleWood:teak);
frontGlass(-4.08,-.50,1.28,3.81,4.93,3);
// Tall feature window, cut out from the front wood-brown panel area
box(2.48,4.28,4.80,.32,6.52,.21,stucco);
frontGlass(2.65,3.40,1.29,6.83,4.97,1);
box(3.01,3.93,5.06,.75,.06,.10,black);
// Tall walnut frame + warm slatted architectural accent
box(4.32,4.36,4.84,1.77,6.89,.23,walnut);
for(let i=0;i<14;i++)box(3.51+i*.119,4.35,4.995,.044,6.75,.065,(i%3===0)?paleWood:teak);
box(5.25,4.28,4.82,.15,6.93,.31,cream);
// Upper-level front wall and door, partially visible behind balcony
box(1.03,6.29,4.75,2.58,2.50,.19,stucco);
frontGlass(.35,1.70,5.24,7.12,4.89,2);
box(2.17,6.22,4.80,.72,2.71,.18,cream);

// Over-glass interior: visible living room and cabinetry.
box(-2.42,1.46,3.08,2.06,.25,.80,fabric);
box(-2.42,1.89,2.75,2.06,.73,.18,fabric);
for(const xx of [-3.19,-1.65])box(xx,1.76,3.08,.18,.65,.77,cushion);
box(-2.38,1.88,2.84,.52,.28,.12,cushion);
box(-2.44,1.25,3.91,1.26,.11,.55,walnut);
for(const xx of [-2.95,-1.96])for(const zz of [3.69,4.12])box(xx,1.06,zz,.08,.30,.08,charcoal);
box(-.05,2.02,2.37,2.00,.19,.84,cream);
box(-.05,1.48,2.43,1.88,.88,.70,walnut);
for(let i=0;i<3;i++){
  const x=-.58+i*.58;cyl(x,1.35,3.30,.16,.16,.08,black);cyl(x,1.16,3.30,.035,.035,.27,charcoal);
}
// Wall cabinetry and pendant lights inside
box(-.45,2.66,1.1,2.1,1.13,.35,teak);
for(let i=0;i<3;i++)box(-1.06+i*.61,2.66,1.30,.016,.9,.035,walnut);
for (const xx of [-2.4,-.35]){
  rod([xx,3.9,2.6],[xx,3.27,2.6],.018,charcoal);
  cyl(xx,3.25,2.6,.26,.10,.12,warmLight);
}
// floor interior warm inset
box(-2.32,1.034,2.20,5.05,.025,4.65,mat('#b99979'));

// Right facade: glass openings in the segmented wall, showing a dark interior.
for(const [zc,ww] of [[1.65,1.90],[-1.65,1.90]]){
  box(5.37,2.65,zc,.050,2.10,ww+.22,black);
  box(5.409,2.65,zc,.035,2.01,ww+.08,darkGlass,scene,false);
  for(const pz of [zc-ww/2,zc,zc+ww/2])box(5.44,2.65,pz,.062,2.14,.056,charcoal);
  for(const yy of [1.59,3.68])box(5.44,yy,zc,.063,.066,ww+.20,charcoal);
}

// Second floor roof terrace (left half), white cantilever and clean soffit.
box(-2.26,4.54,.35,6.60,.38,10.63,white);
box(-2.26,4.755,.35,6.60,.07,10.64,mat('#a9957f'));
box(-2.26,4.40,5.57,6.70,.43,.36,white);
// Wood ceiling visible under projecting roof-deck edge
box(-2.31,4.325,5.33,6.53,.07,.44,walnut);
for(let i=0;i<15;i++)box(-5.39+i*.43,4.282,5.29,.022,.016,.55,paleWood);

// Railings: front and left balcony. Rail posts at consistent intervals.
function balconyFrontRail(z,x0,x1,base=4.80){
 for(let i=0;i<=7;i++){const x=x0+(x1-x0)*i/7;box(x,base+.58,z,.065,1.16,.07,charcoal);}
 for(const y of [base+.10,base+.40,base+.72,base+1.14])box((x0+x1)/2,y,z,x1-x0+.07,.038,.043,charcoal);
}
balconyFrontRail(5.73,-5.53,.80);
for(let i=0;i<=5;i++)box(-5.53,5.39,-4.66+i*2.07,.07,1.16,.07,charcoal);
for(const y of [4.90,5.20,5.52,5.94])box(-5.53,y,.50,.048,.04,10.40,charcoal);
// Terrace potted plants and cafe seating
function pot(x,y,z,size=1){
  cyl(x,y+.25*size,z,.245*size,.18*size,.50*size,concrete);
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4, p=new THREE.Vector3(x,y+.45*size,z),e=p.clone().add(new THREE.Vector3(Math.cos(a)*.45*size,.47*size,Math.sin(a)*.45*size));
    leaf(p,e,.15*size,i%2?leaf1:leaf2);
  }
}
pot(-4.95,4.78,4.45,1.05);pot(.05,4.78,4.18,.88);pot(-4.90,4.78,-3.90,.82);
// metal chairs and coffee table on deck
cyl(-2.93,5.19,2.07,.54,.54,.065,walnut);
cyl(-2.93,4.98,2.07,.055,.055,.42,charcoal);
function chair(x,y,z,rotation=0){
  const g=new THREE.Group();g.position.set(x,y,z);g.rotation.y=rotation;scene.add(g);
  box(0,.40,0,.69,.10,.64,teak,g);
  box(0,.76,-.31,.69,.67,.09,charcoal,g);
  for(let xx of [-.28,.28])for(let zz of [-.23,.23])box(xx,.19,zz,.053,.39,.05,charcoal,g);
}
chair(-4.13,4.79,2.05,-Math.PI/2);chair(-1.72,4.79,2.05,Math.PI/2);chair(-2.93,4.79,.95,0);
// Small lounge near entrance porch
box(-2.93,.85,5.56,2.15,.20,.88,teak);
box(-2.93,1.18,5.25,2.09,.49,.17,fabric);
box(-2.93,1.10,5.54,1.89,.15,.61,cushion);
for(const xx of [-3.82,-2.03])box(xx,1.00,5.57,.12,.27,.80,walnut);
cyl(-1.34,.99,5.83,.32,.32,.07,walnut);cyl(-1.34,.75,5.83,.037,.037,.43,charcoal);

// Roof: slender asymmetric black single-slope canopy over right volume.
const roofGroup=new THREE.Group(); roofGroup.position.set(2.78,7.75,-.2);roofGroup.rotation.x=-.060;scene.add(roofGroup);
box(0,-.12,0,6.54,.17,11.22,walnut,roofGroup);
box(0,.03,0,6.75,.24,11.51,black,roofGroup);
box(0,-.16,5.62,6.58,.10,.11,charcoal,roofGroup);
// under-roof wood strips visible from the street
for(let i=0;i<22;i++)box(-2.99+i*.28,-.218,4.69,.034,.023,1.19,paleWood,roofGroup);

// Warm exterior wall sconces and recessed spot lights
const decorativeLights=[];
function addSconce(x,y,z){
  box(x,y,z,.16,.54,.18,charcoal);
  sphere(x,y+.26,z+.1,.075,warmLight);
  sphere(x,y-.28,z+.1,.065,warmLight);
  const l=new THREE.PointLight('#ffd39d',1.2,4.2,2);l.position.set(x,y+.12,z+.47);scene.add(l);decorativeLights.push(l);
}
addSconce(-4.62,2.48,5.09);addSconce(4.29,4.24,5.07);
function recessed(x,y,z){disk(x,y,z,.073,whiteLight);}
for(const x of [-4.6,-3.2,-1.65,-.1])recessed(x,4.28,5.46);
for(const x of [.28,1.65,3.15,4.75])recessed(x,7.47,5.00);

// Front steps aligned to right-side entry
const stairX=1.25;
for(let i=0;i<5;i++){
  const h=.16*(i+1),z=7.58-i*.40;
  box(stairX,h/2,z,2.7,h,.44,stone);
  box(stairX,h+.025,z,2.7,.05,.44,concrete);
  box(stairX,h+.013,z+.23,2.54,.02,.023,whiteLight);
}
for(const x of [stairX-1.43,stairX+1.43]){
  for(let i=0;i<3;i++){
    const z=7.62-i*.74,y=.25+i*.32;
    rod([x,y,z],[x,y+.78,z],.036,charcoal);
  }
  rod([x,.99,7.62],[x,1.66,6.09],.049,charcoal);
}

// Landscaped front garden: two long low planter beds
function frontBed(a,b){
  box((a+b)/2,.35,6.61,b-a,.63,1.23,charcoal);
  box((a+b)/2,.69,6.61,b-a-.15,.055,1.04,soil);
  for(let x=a+.30;x<b-.21;x+=.59){
    bush(x,.82,6.58,ranged(.23,.38));
    if(rand()>.64)spikyPlant(x+.12,.77,6.65,.60);
  }
}
function bush(x,y,z,r){
  for(let j=0;j<6;j++)sphere(x+ranged(-r*.4,r*.4),y+ranged(0,r*.52),z+ranged(-r*.4,r*.4),r*ranged(.43,.70),j%2?leaf1:leaf3);
}
function leaf(from,to,width,material){
  const a=from.clone(),b=to.clone(),dir=b.clone().sub(a),side=new THREE.Vector3(-dir.z,.22*dir.length(),dir.x).normalize().multiplyScalar(width);
  const p=a.clone().add(dir.clone().multiplyScalar(.48)).add(new THREE.Vector3(0,.10*dir.length(),0));
  const coords=[...a.toArray(),...p.clone().add(side).toArray(),...b.toArray(), ...a.toArray(),...b.toArray(),...p.clone().sub(side).toArray()];
  const geom=new THREE.BufferGeometry(); geom.setAttribute('position',new THREE.Float32BufferAttribute(coords,3));geom.computeVertexNormals();
  const m=new THREE.Mesh(geom,material);m.castShadow=true;scene.add(m);return m;
}
function spikyPlant(x,y,z,sc=1){
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4,base=new THREE.Vector3(x,y,z),end=new THREE.Vector3(x+Math.cos(a)*.53*sc,y+ranged(.23,.70)*sc,z+Math.sin(a)*.53*sc);
    leaf(base,end,.17*sc,i%2?leaf1:leaf2);
  }
}
frontBed(-5.25,-.35);frontBed(2.85,5.4);
for(let i=0;i<55;i++){
  const x=ranged(-8.7,8.7),z=ranged(-5.0,7.1);
  if(x>-5.5&&x<5.5)continue;
  if(rand()>.47)bush(x,.24,z,ranged(.17,.40));else spikyPlant(x,.16,z,ranged(.55,.91));
}
// Modern low front gate and boundary walls; central opening shows the stairs.
box(-9.40,.85,7.97,1.25,1.72,.31,cream);
box(9.40,.85,7.97,1.25,1.72,.31,cream);
box(-7.09,.65,7.97,3.44,1.23,.24,cream);
box(6.72,.65,7.97,3.72,1.23,.24,cream);
function fence(x0,x1,z){
  for(let x=x0;x<=x1+.01;x+=1.25)box(x,.88,z,.16,1.55,.20,stucco);
  for(const yy of [.46,.80,1.14,1.50])box((x0+x1)/2,yy,z+.13,x1-x0,.032,.045,charcoal);
}
fence(-5.30,-.25,8.09); fence(2.83,5.43,8.09);
for(let x=5.55;x<9.0;x+=.22)box(x,.92,8.08,.07,1.14,.07,charcoal);
// Rear perimeter / side walls intentionally short so the camera can see the house.
box(-9.80,.75,-3.1,.26,1.50,22.1,cream);
box(9.80,.75,-3.1,.26,1.50,22.1,cream);
box(0,.78,-13.94,19.75,1.56,.25,cream);

// ─── Front carport: Option A front facade, no swimming pool here ──────
// Covered parking bay on the front-left side of the house (front = positive Z).
box(-7.63,.09,4.08,3.85,.13,6.67,ivoryTile);
box(-7.54,3.86,4.60,4.45,.22,6.90,black);
box(-7.54,3.72,4.57,4.24,.12,6.64,walnut);
for(let i=0;i<12;i++)box(-9.49+i*.36,3.645,4.65,.04,.016,6.40,paleWood);
for(const x of [-9.31,-5.80]){
  box(x,2.05,7.77,.21,3.42,.24,stucco);
  box(x,2.05,1.43,.21,3.42,.24,stucco);
}
// Car: stylized premium SUV, fully 3D and visible through the gate.
function vehicle(x,z){
  const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
  const body=mat('#eeeeea',{roughness:.31,metalness:.44});
  const windows=mat('#1f3944',{roughness:.10,metalness:.23});
  box(0,.91,0,2.15,.66,4.16,body,g);
  box(0,1.48,-.11,1.98,.70,2.64,body,g);
  box(0,1.76,-.11,1.88,.13,2.28,body,g);
  for(const sx of [-1,1]){
    box(sx*.996,1.46,-.08,.037,.56,2.0,windows,g);
    for(const sz of [-1.41,1.48]){
      const wheel=cyl(sx*1.06,.58,sz,.43,.43,.24,charcoal,g,22);
      wheel.rotation.z=Math.PI/2;
      const rim=cyl(sx*1.185,.58,sz,.25,.25,.245,concrete,g,18);rim.rotation.z=Math.PI/2;
    }
  }
  box(0,1.48,-1.48,1.80,.55,.042,windows,g);
  box(0,1.48,1.45,1.78,.52,.04,windows,g);
  for(const sx of [-.74,.74]){
    box(sx,1.05,2.10,.42,.18,.065,warmLight,g);
    box(sx,.93,-2.11,.45,.14,.065,mat('#bc3333'),g);
  }
}
vehicle(-7.58,4.03);
// Long simple wood-slat driveway gate (inside wall, leaving pedestrian gate area).
for(let x=-9.0;x<-5.55;x+=.17)box(x,.92,8.22,.075,1.55,.10,walnut);
box(-7.3,1.70,8.24,3.72,.08,.12,charcoal);
box(-7.3,.22,8.24,3.72,.10,.12,charcoal);

// ─── Rear architectural conversion: Option C resort-style pool terrace ─
// Finished rear patio continuous with both rear sliding doors.
box(0,.87,-5.49,10.3,.23,1.73,ivoryTile);
for(let i=0;i<21;i++)box(-5.06+i*.50,.994,-5.52,.014,.011,1.65,concrete);
// Large timber pergola over the right-side outdoor lounge.
for(const x of [2.10,4.93])for(const z of [-5.05,-7.06]){
  box(x,2.58,z,.17,3.04,.18,walnut);
}
for(let i=0;i<10;i++)box(2.0+i*.32,4.13,-6.07,.065,.16,2.65,paleWood);
box(3.50,4.02,-6.04,3.18,.14,2.55,walnut);
// Timber deck along the pool on its right side.
box(4.45,.13,-9.50,3.06,.18,6.70,walnut);
for(let i=0;i<24;i++)box(2.98+i*.123,.233,-9.5,.018,.011,6.60,paleWood);
// Outdoor luxury sofa set near the pool.
box(4.30,.51,-8.30,2.25,.21,.83,fabric);
box(4.30,.86,-8.68,2.26,.65,.15,walnut);
for(const x of [3.38,5.22])box(x,.65,-8.28,.14,.34,.79,walnut);
for(const x of [3.73,4.40,5.03])box(x,.70,-8.30,.56,.22,.65,cushion);
box(4.40,.50,-10.37,1.12,.14,.65,teak);
for(const x of [3.99,4.81])for(const z of [-10.12,-10.62])box(x,.28,z,.05,.42,.055,charcoal);
// Pair of loungers facing the swimming pool.
for(const zz of [-11.45,-6.98]){
  box(4.45,.40,zz,.91,.11,1.51,walnut);
  box(4.45,.49,zz,.84,.12,1.37,cushion);
  box(4.45,.74,zz-.61,.85,.57,.12,cushion);
}
// Upper rear cantilever balcony above covered dining terrace.
box(2.38,4.72,-5.72,6.05,.24,2.00,white);
box(2.38,4.855,-5.72,6.05,.04,1.98,stone);
for(const x of [-.48,5.18])box(x,2.82,-6.47,.15,3.63,.15,stucco);
// Clear rear glass railings -- distinctly different from the dark front rails.
const railGlass = new THREE.MeshPhysicalMaterial({color:'#c9e8e8',roughness:.05,metalness:.08,transparent:true,opacity:.26,side:THREE.DoubleSide,depthWrite:false});
box(2.35,5.48,-6.70,5.90,1.05,.038,railGlass,scene,false);
for(const x of [-.54,1.38,3.33,5.24])box(x,5.47,-6.71,.065,1.12,.09,charcoal);
box(2.34,6.035,-6.71,5.92,.035,.08,charcoal);
box(5.30,5.45,-5.71,.05,1.05,1.98,railGlass,scene,false);
// Large rectangular pool centered in the *backyard only*.
const poolX=-.65,poolZ=-9.56,poolW=5.60,poolD=6.14;
box(poolX,.06,poolZ,poolW+1.12,.21,poolD+1.02,ivoryTile);
box(poolX,.173,poolZ,poolW+.08,.025,poolD+.06,polishedStone);
box(poolX,.183,poolZ,poolW-.22,.025,poolD-.22,poolTile);
// Blue pool floor base with lower step silhouettes.
box(poolX,.198,poolZ,poolW-.35,.014,poolD-.35,poolTile);
for(let i=0;i<4;i++)box(poolX-poolW/2+.35+i*.31,.204,poolZ+poolD/2-.55, .31,.025,.78,mat('#45a9ae'));
const waterGeometry=new THREE.PlaneGeometry(poolW-.35,poolD-.35,42,48);
waterGeometry.rotateX(-Math.PI/2);
const waterSurface=new THREE.Mesh(waterGeometry,azure);waterSurface.position.set(poolX,.224,poolZ);waterSurface.receiveShadow=true;scene.add(waterSurface);
// White travertine coping laid around the water, no mesh covering the surface.
for(const side of [-1,1]){
  box(poolX+side*(poolW/2+.18),.275,poolZ,.35,.12,poolD+.75,ivoryTile);
  box(poolX,.275,poolZ+side*(poolD/2+.17),poolW+.72,.12,.36,ivoryTile);
}
// Tiny underwater lights with soft cyan glow.
for(const x of [-2.30,1.17])for(const z of [-11.4,-8.2]){
  const m=cyl(x,.247,z,.084,.084,.021,blueLight);m.rotation.x=Math.PI/2;
}
// Feature wall with streaming waterfall across the far edge of pool.
box(-1.87,1.00,-12.94,2.70,1.78,.34,polishedStone);
for(let i=0;i<18;i++)box(-3.12+i*.141,1.00,-12.743,.014,1.59,.034,i%4===0?stone:concrete);
box(-1.87,1.77,-12.69,2.66,.12,.25,charcoal);
const fallMat=new THREE.MeshPhysicalMaterial({color:'#a0e8ef',emissive:'#23a8ce',emissiveIntensity:.25,transparent:true,opacity:.54,roughness:.13,side:THREE.DoubleSide,depthWrite:false});
const falls=[];
for(let i=0;i<15;i++){
  const x=-3.06+i*.17;
  const strip=box(x,.97,-12.53,.095,1.43,.020,fallMat,scene,false);
  falls.push(strip);
}
for(let i=0;i<13;i++)sphere(-3.01+i*.186,.255+ranged(0,.10),-12.48,.07,mat('#aff6fa',{transparent:true,opacity:.70}));
// Poolside landscaped zones with planter lighting.
for(let i=0;i<11;i++){
  const z=-12.38+i*.50;
  bush(-4.88,.26,z,.33);
  if(i%2===0)spikyPlant(-5.27,.23,z,.68);
}
for(const [x,z] of [[-4.87,-11.6],[-4.86,-8.5],[5.72,-12.20],[5.65,-6.45]]){
  cyl(x,.32,z,.075,.075,.64,charcoal);
  sphere(x,.71,z,.11,warmLight);
}
// ─── Taller palm trees with tropical layered fronds ────────────────────
function palm(x,z,height=5.5){
  const group=new THREE.Group();group.position.set(x,0,z);scene.add(group);
  let bottom=new THREE.Vector3(0,.0,0);
  for(let i=0;i<12;i++){
    const t=(i+1)/12;
    const top=new THREE.Vector3(-.17*t,height*t,.15*t);
    rod([bottom.x,bottom.y,bottom.z],[top.x,top.y,top.z],.13*(1-.48*t),mat(i%2?'#76573a':'#916b48'),group);
    bottom=top;
  }
  const crown=new THREE.Vector3(-.17,height,.15);
  for(let j=0;j<10;j++){
    const a=j*Math.PI*2/10,length=ranged(1.8,2.52);
    const end=crown.clone().add(new THREE.Vector3(Math.cos(a)*length,-.65,Math.sin(a)*length));
    const mid=crown.clone().lerp(end,.53).add(new THREE.Vector3(0,.45,0));
    const curve=new THREE.QuadraticBezierCurve3(crown,mid,end);
    const points=curve.getPoints(10);
    for(let k=0;k<10;k++)rod([points[k].x,points[k].y,points[k].z],[points[k+1].x,points[k+1].y,points[k+1].z],.016,leaf3,group);
    for(let k=1;k<10;k++){
      const p=curve.getPoint(k/11),radial=new THREE.Vector3(-Math.sin(a),0,Math.cos(a));
      for(const sign of [-1,1]){
        const tip=p.clone().addScaledVector(radial,sign*(.46-.017*k));tip.y-=.20+.11*k/10;
        const origin=new THREE.Vector3(x+p.x,p.y,z+p.z);
        const tipworld=new THREE.Vector3(x+tip.x,tip.y,z+tip.z);
        leaf(origin,tipworld,.095,k%3?leaf1:leaf2);
      }
    }
  }
}
palm(-8.3,2.6,5.75);palm(-7.95,-4.4,6.45);palm(8.2,-2.3,6.2);
// Ground-level accent lights and small planters
function bollard(x,z){
  cyl(x,.24,z,.06,.06,.48,charcoal);
  cyl(x,.53,z,.13,.09,.16,warmLight);
  const l=new THREE.PointLight('#ffc782',.6,2.3,2);l.position.set(x,.63,z);scene.add(l);decorativeLights.push(l);
}
for(const [x,z] of [[-5.25,6.77],[-3.63,6.76],[-1.08,6.78],[3.27,6.79],[5.25,6.75],[8.45,2.3]])bollard(x,z);
for(const [x,z,sz] of [[-4.7,5.65,.9],[2.55,5.51,.78],[6.55,1.7,.90]])pot(x,.76,z,sz);

// Rear waterfall and pool accent lighting; controlled by Day / Dusk mode.
for(const [x,z] of [[-1.5,-12.3],[2.5,-12.1],[-4.5,-8.7],[4.4,-7.6]]){
  const lamp=new THREE.PointLight('#63ddea',.55,4.1,2);
  lamp.position.set(x,.64,z);scene.add(lamp);decorativeLights.push(lamp);
}
// Palm tree pair beyond rear pool, near back perimeter.
palm(-7.55,-10.75,7.3);palm(7.26,-11.12,6.8);

// ─── Day / dusk lighting switches ───────────────────────────────────────
const skyLight=new THREE.HemisphereLight('#dce8ff','#6a6a60',2.1);scene.add(skyLight);
const ambient=new THREE.AmbientLight('#f1e4d4',.8);scene.add(ambient);
const sunlight=new THREE.DirectionalLight('#ffe0af',3.0);sunlight.position.set(-11,19,13);sunlight.castShadow=true;
sunlight.shadow.mapSize.set(2048,2048);
sunlight.shadow.camera.left=-22; sunlight.shadow.camera.right=22;
sunlight.shadow.camera.top=22; sunlight.shadow.camera.bottom=-22;
sunlight.shadow.camera.near=1; sunlight.shadow.camera.far=65;
sunlight.shadow.bias=-0.00015;scene.add(sunlight);
let isDusk=true;
function setLighting(mode){
  isDusk=mode==='dusk';viewport.classList.toggle('day',!isDusk);
  sunlight.intensity=isDusk?2.15:3.65; sunlight.color.set(isDusk?'#ffbf93':'#fff7de');
  skyLight.intensity=isDusk?1.7:2.7; ambient.intensity=isDusk?.76:1.05;
  decorativeLights.forEach(l=>l.intensity=isDusk?(l.userData.baseIntensity??l.intensity):0);
  renderer.toneMappingExposure=isDusk?1.36:1.43;
  document.querySelectorAll('[data-mode]').forEach(btn=>btn.classList.toggle('active',btn.dataset.mode===mode));
}
decorativeLights.forEach(l=>l.userData.baseIntensity=l.intensity);
setLighting('dusk');

// ─── Camera controls, UI interaction, resize, render loop ────────────────
function setView(which='angle'){
  camera.position.set(...cameraPositions[which]);controls.target.copy(which==='back'||which==='pool'?poolTarget:target);controls.update();
  document.querySelectorAll('[data-view]').forEach(btn=>btn.classList.toggle('active',btn.dataset.view===which));
}
setView('angle');
document.querySelectorAll('[data-view]').forEach(btn=>btn.addEventListener('click',()=>setView(btn.dataset.view)));
document.querySelectorAll('[data-mode]').forEach(btn=>btn.addEventListener('click',()=>setLighting(btn.dataset.mode)));
document.getElementById('reset').addEventListener('click',()=>setView('angle'));
function resize(){const w=viewport.clientWidth,h=viewport.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h);}
addEventListener('resize',resize);
const waveBase=waterGeometry.attributes.position.array.slice();
const waterPosition=waterGeometry.attributes.position;
const clock = new THREE.Clock();
renderer.setAnimationLoop(()=>{
  const time=clock.getElapsedTime();
  for(let i=0;i<waterPosition.count;i++){
    const j=i*3, px=waveBase[j],pz=waveBase[j+2];
    waterPosition.array[j+1]=.017*Math.sin(px*2.6+time*1.65)*Math.cos(pz*2.3-time*1.24);
  }
  waterPosition.needsUpdate=true;
  for(let i=0;i<falls.length;i++)falls[i].scale.y=0.96+.07*Math.sin(time*2.4+i*.7);
  controls.update();renderer.render(scene,camera);
});
