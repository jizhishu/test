# Create your views here.
import models
try:
    p = models.Publisher.objects.get(name='Apress')
except models.Publisher.DoesNotExist:
    print "Apress isn't in the database yet."
else:
    print "Apress is in the database."