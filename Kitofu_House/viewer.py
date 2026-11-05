"""Run with: python viewer.py. All geometry is local and procedural."""
import argparse
import time
from html import escape


def main():
    parser=argparse.ArgumentParser(description='KITOFU HOUSE — interactive VPython final project')
    parser.add_argument('--low-detail',action='store_true',help='Reduce palms and decorative slats')
    parser.add_argument('--smoke-seconds',type=float,default=0,help='Exit after this many animation seconds (verification only)')
    args=parser.parse_args()
    try:
        import vpython as v
    except ImportError as exc:
        raise SystemExit('VPython is not installed in this interpreter. Run: python -m pip install -r requirements.txt') from exc
    from house import config as C
    if args.low_detail: C.DETAIL='low'
    from house.geometry import Builder, color
    from house import architecture, interiors, landscape, vehicles, controls
    from house.dog import Dog
    from house.cameras import Cameras
    scene=v.canvas(title='<div style="background:#f3eee3;color:#233c32;padding:20px 24px;border-top:5px solid #233c32">'
                         '<small>THE PRIVATE RESIDENCE COLLECTION / PHILIPPINES</small>'
                         f'<h1>{escape(C.TITLE)}</h1> TROPICAL ARCHITECTURE · WARM INTERIORS<br>'
                         'Two floors. A generous front garden. A private backyard retreat.</div>',
                   width=C.VIEW_WIDTH,height=C.VIEW_HEIGHT,background=color((.78,.86,.87)),
                   ambient=color((.48,.48,.44)),autoscale=False)
    scene.range=35
    scene.lights=[]
    sun=v.distant_light(direction=v.vector(-.5,1,-.4),color=color((.75,.72,.64)))
    fill=v.distant_light(direction=v.vector(.5,.3,.7),color=color((.25,.3,.33)))
    print('Building KITOFU HOUSE. Keep this terminal open; VPython opens your browser.',flush=True)
    builder=Builder()
    landscape_lights=landscape.build(builder)
    architecture.build(builder)
    interiors.build(builder)
    vehicles.build(builder)
    dog=Dog()
    camera=Cameras(scene,builder.obstacles,dog)
    controls.build(scene,camera,builder,dog,landscape_lights,sun,fill)
    if args.smoke_seconds:
        # Integration checks use actual VPython objects, not renderer mocks.
        sizes=[v.vector(obj.size) for obj,_ in dog.parts+dog.legs+dog.tail]
        dog.update(.1)
        assert all(v.mag(obj.size-size)<1e-9
                   for (obj,_),size in zip(dog.parts+dog.legs+dog.tail,sizes))
        dog.paused=True; position=v.vector(dog.pos); dog.update(.1)
        assert v.mag(dog.pos-position)<1e-9
        dog.paused=False
        builder.cutaway('Ground floor')
        assert all(obj.visible for obj in builder.groups['ground'])
        assert all(not obj.visible for obj in builder.groups['upper']+builder.groups['roof'])
        builder.cutaway('Roof off')
        assert all(obj.visible for obj in builder.groups['upper'])
        assert all(not obj.visible for obj in builder.groups['roof'])
        builder.cutaway('Full exterior')
        assert all(obj.visible for obj in builder.groups['roof'])
        print('Real-object checks passed: pet dimensions, pause and cutaway visibility.',flush=True)
    print(f'Ready: {builder.count} construction primitives before compounding; '
          f'{len(builder.obstacles)} collision volumes. Ctrl+C stops the project.',flush=True)
    previous=time.perf_counter(); elapsed=0
    try:
        while True:
            v.rate(C.FPS)
            now=time.perf_counter(); dt=min(.05,max(0,now-previous)); previous=now
            elapsed+=dt
            dog.update(dt); camera.update(dt)
            landscape.animate(elapsed)
            if args.smoke_seconds and elapsed>=args.smoke_seconds:
                print('Smoke run completed without an exception.',flush=True)
                break
    except KeyboardInterrupt:
        print('\nKITOFU HOUSE stopped.')


if __name__=='__main__':
    main()
