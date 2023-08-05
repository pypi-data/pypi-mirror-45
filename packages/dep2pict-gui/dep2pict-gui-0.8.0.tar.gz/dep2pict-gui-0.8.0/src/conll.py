import tempfile
import subprocess

def load_conll (filename):
    reset()
    sent_id_list = []
    sentence_offset_dict = dict()
    fo = open(filename, "r", encoding='utf8')
    lines = fo.read().splitlines()
    fo.close()
    sent=None
    current_linenum=0
    next_sent_linenum=0
    for l in lines:
        if l == '':
            if sent != None and (not all(l[0] == "#" for l in sent)): # end
                sent_id = get_sentid (sent)
                if sent_id in sentence_offset_dict:
                    raise ValueError('Duplicate sent_id "%s" (line %d)' % (sent_id, current_linenum))
                else:
                    sentence_offset_dict[sent_id] = (sent, next_sent_linenum)
                    sent_id_list = sent_id_list + [sent_id]
                sent = None
        else: # empty line
            if sent == None:
                sent = [l]
                next_sent_linenum=current_linenum
            else:
                sent = sent+[l]
        current_linenum += 1
    return (sent_id_list, sentence_offset_dict)

next_automatic_sent_id = 0
def reset():
    global next_automatic_sent_id
    next_automatic_sent_id=0

def new_id():
    global next_automatic_sent_id
    next_automatic_sent_id+=1
    return ("%05d" % next_automatic_sent_id)

def get_sentid(sentence):
    try:
        sent_id_line = next(l for l in sentence if l[0]=="#" and "# sent_id =" in l)
        return (sent_id_line.split (" = "))[1]
    except StopIteration:
        return new_id()

def get_text(sentence):
    try:
        sent_id_line = next(l for l in sentence if l[0]=="#" and "# text =" in l)
        return (sent_id_line.split (" = "))[1]
    except StopIteration:
        return None

def to_svg(sentence):
    with tempfile.NamedTemporaryFile('w', suffix=".conllu", encoding='utf8') as temp:
        conllu=temp.name
        svg=conllu.replace('conllu', 'svg')
        for l in sentence:
            temp.write(l+"\n")
        temp.flush()
        err= ""
        sub=subprocess.run (["dep2pict","--batch",conllu,svg], stderr=subprocess.PIPE)
        if sub.returncode != 0:
            return sub.stderr.decode("utf-8")
    return svg
