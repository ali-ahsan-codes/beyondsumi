"""Per-film motion/lip-sync choices and image-call budgets. No generation or approval."""
import re

DEFAULT_STATES = {'sumi-original': 20, 'sumi-light': 12, 'sumi-dark': 12}
NOTICE = 'Extra pose/in-between artwork may require more image calls, tokens, cost and processing time; estimate each batch before generation.'

def _text(value):
    return isinstance(value, str) and bool(value.strip())

def smooth_24(data):
    c = data.get('motion_detail', {})
    return (isinstance(c, dict) and c.get('art_route') == 'images'
            and c.get('mode') == 'smooth24' and c.get('status') == 'approved'
            and _text(c.get('approval_record')))

def initial_choice(style, art_route='images'):
    return {'schema': 1, 'art_route': art_route,
            'mode': 'default' if art_route == 'svg' else 'pending',
            'status': 'not-applicable' if art_route == 'svg' else 'pending',
            'default_states_per_second': DEFAULT_STATES[style],
            'target_states_per_second': DEFAULT_STATES[style],
            'approval_record': '', 'resource_notice': NOTICE,
            'image_batches': [], 'reuse_only_reason': ''}

def validate(data, root=None, stage='assets'):
    version = tuple(map(int, re.findall(r'\d+', str(data.get('release_version', '0.0.0')))))
    if 'motion_detail' not in data and version < (5, 1, 3):
        return []
    errors = []
    def need(ok, message):
        if not ok: errors.append('Production choices: ' + message)
    c = data.get('motion_detail')
    if not isinstance(c, dict):
        return ['Production choices: record this film’s motion choice; SVG retains its default without that prompt']
    route = c.get('art_route'); need(route in {'images', 'svg'}, 'choose image or SVG artwork')
    default = DEFAULT_STATES.get(data.get('style'))
    need(c.get('default_states_per_second') == default, 'show the selected style’s actual default')
    if route == 'svg':
        need(c.get('mode') == 'default' and c.get('status') == 'not-applicable'
             and c.get('target_states_per_second') == default, 'SVG keeps its existing default; no smoothness upsell/prompt')
        need(not c.get('image_batches'), 'SVG-only projects must not contain unapproved image calls')
    elif route == 'images':
        need(c.get('mode') in {'default', 'smooth24'} and c.get('status') == 'approved'
             and _text(c.get('approval_record')), 'ask for default or smoother motion on every new image-based film and record the answer')
        target = 24 if c.get('mode') == 'smooth24' else default
        need(c.get('target_states_per_second') == target, 'selected character-state target differs from the choice')
        need(_text(c.get('resource_notice')), 'disclose possible additional artwork/calls/tokens/time')
        batches = c.get('image_batches', [])
        need(isinstance(batches, list), 'image_batches must be a list')
        if isinstance(batches, list):
            need(bool(batches) or _text(c.get('reuse_only_reason')), 'budget each separate image call/batch, or explain exact compatible reuse')
            ids = set()
            for batch in batches:
                if not isinstance(batch, dict):
                    need(False, 'image batch must be an object'); continue
                bid = batch.get('id'); need(_text(bid) and bid not in ids, 'image batch IDs must be unique'); ids.add(str(bid))
                need(_text(batch.get('approval_record')), 'each standalone image call/batch needs its approved scope')
                need(_text(batch.get('purpose')), 'image batch must describe its poses/in-betweens/mouth shapes')
                for key in ['new_pose_drawings', 'image_calls_max']:
                    value = batch.get(key); need(type(value) is int and value >= 0, key + ' must be a separate non-negative budget')
                used = batch.get('actual_image_calls', 0); limit = batch.get('image_calls_max')
                need(type(used) is int and used >= 0 and type(limit) is int and used <= limit,
                     'image calls exceed approval; stop and ask before increasing the budget')
    dialogue = data.get('dialogue_animation', {})
    if not isinstance(dialogue, dict): dialogue = {}
    mode = dialogue.get('speech_mode'); sync = dialogue.get('lip_sync')
    need(mode in {'narration-only', 'dialogue', 'both', 'none'}, 'confirm narration/dialogue/both/none for this video')
    need(_text(dialogue.get('approval_record')), 'record this video’s dialogue/lip-sync choice')
    if mode in {'dialogue', 'both'}:
        need(sync in {'on', 'off'}, 'offer visible-speaker lip-sync and record on/off before artwork')
        if sync == 'on': need(_text(dialogue.get('voice_map')), 'lip-sync needs the role/final-audio map')
    elif mode in {'narration-only', 'none'}:
        need(sync == 'not-applicable', 'do not animate unrelated mouths to offscreen narration or silence')
    return errors
