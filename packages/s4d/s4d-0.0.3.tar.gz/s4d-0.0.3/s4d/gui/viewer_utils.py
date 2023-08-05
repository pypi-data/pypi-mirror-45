import logging
import copy
from s4d.diar import Diar, Segment
from s4d.scoring import DER


def add_match(ref, hyp, assign, not_assigned):
    inv_map = {v: k for k, v in assign.items()}
    i = 0

    l = 0
    for cluster in ref.unique('cluster'):
        if len(cluster) > l:
            l = len(cluster)
    for cluster in hyp.unique('cluster'):
        if len(cluster) > l:
            l = len(cluster)
    f = 'Match {:03d} {:>'+str(l)+'s}'
    for key in sorted(inv_map, reverse=True):
        v = inv_map[key]
        r = v[0]
        h = v[1]
        nr = f.format(i, r)
        nh = f.format(i, h)
        ref.rename('cluster', [r], nr)
        hyp.rename('cluster', [h], nh)
        i += 1
    f = 'NotMatch {:>'+str(l)+'s}'
    for h in not_assigned:
        nh = f.format(h)
        hyp.rename('cluster', [h], nh)


def add_intersection(ref, hyp, assign):
        diar = Diar()
        if not diar._attributes.exist('color'):
            diar.add_attribut('color', (0.0, 0.0, 0.0, 1.0))
        map_ref = ref.make_index(['cluster'])
        map_hyp = hyp.make_index(['cluster'])
        for (lr, lh) in assign:
            for seg1 in map_ref[lr]:
                f = False
                stop = seg1['stop']
                for Seg2 in map_hyp[lh]:
                    if stop < Seg2['start']:
                        continue
                    inter1 = Segment.intersection(seg1, Seg2)
                    if inter1 is not None :
                        f = True
                        inter1['color'] = (0.6, 0.0, 1.0, 1.0)
                        inter1['cluster'] = seg1['cluster']
                        diar.append_seg(inter1)
                        inter2 = copy.deepcopy(inter1)
                        inter2['color'] = (0.0, 0.6, 1.0, 1.0)
                        inter2['cluster'] = Seg2['cluster']
                        diar.append_seg(inter2)
                    elif f:
                        break
        return diar


def add_prefix(diar, prefix):
    for seg in diar:
        seg['cluster'] = prefix+seg['cluster']


def add_collar(diar, collar):
    local_diar = Diar()
    local_diar.add_attribut('color', (0.2, 0.2, 0.2, 1.0))
    if local_diar._attributes.exist('type'):
        local_diar.add_attribut('type', 'collar')
    l = len(diar)
    for seg in diar:
        if l % 100 == 0:
            print(l)
        l -= 1
        show = seg['show']
        name = seg['cluster']
        start = seg['start']
        stop = seg['stop']
        local_diar.append(show=show, cluster=name, start=start - collar, stop=start+collar)
        local_diar.append(show=show, cluster=name, start=stop - collar, stop=stop+collar)
    diar.append_diar(local_diar)


def diar_diff(hyp, ref, match=True, inter=False, collar=25):
    hyp = copy.deepcopy(hyp)
    if not hyp._attributes.exist('color'):
        hyp.add_attribut('color', (0.0, 0.6, 0.0, 1.0))
    hyp.pack()

    ref = copy.deepcopy(ref)
    if not ref._attributes.exist('color'):
        ref.add_attribut('color', (0.6, 0.0, 0.0, 1.0))
    ref.pack()

    der = DER(hyp, ref)
    der.confusion()
    assign, not_assign = der.assignment()
    if match:
        add_match(ref, hyp, assign, not_assign)
    else:
        add_prefix(ref, 'REF: ')
        add_prefix(hyp, 'HYP: ')
        
    diar = copy.deepcopy(ref)
    diar.append_diar(hyp)
    
    if inter:
        logging.info('append intersection')
        diar.append_diar(add_intersection(ref, hyp, assign))

    if collar > 0:
        logging.info('append collar')
        add_collar(diar, collar)
    return diar