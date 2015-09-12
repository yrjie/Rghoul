from Rghoul.models import Comment, Comment0
from datetime import datetime

allcmts = Comment0.objects.all()
for x in allcmts:
    ctx = x.context.split("<dd><i>&nbsp;")[0].strip()
    dstr = x.context.split("posted at")[-1].split("</i></dd>")[0].strip()
    dt = datetime.strptime(dstr, "%Y-%m-%d %H:%M:%S")
    cmt = Comment(author=x.author, context=ctx, parent=x.parent, date=dt)
    cmt.save()

print len(allcmts)