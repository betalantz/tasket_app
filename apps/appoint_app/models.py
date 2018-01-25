from __future__ import unicode_literals

from django.db import models
from ..user_app.models import User

# Create your models here.
class AppointManager(models.Manager):
    def appointValidator(self,request, postData):
        results = {'status': True, 'errors': []}

        if not postData['task'] or len(postData['task']) < 1:
            results['errors'].append('Task must be at least 1 character long.')

        try:
            datestr = postData['apt_date']
            taskdate = datetime.datetime.strptime(datestr, "%Y-%m-%d").date()
            if taskdate < date.today():
                results['errors'].append('Appointment cannot be before today.')
        except:
            results["errors"].append("'Date' is a required field.")
       
        if results['status'] == True:
            currUser = User.objects.get(id=request.session['user_id'])
            if len(self.filter(date=postData['apt_date'], time=postData['apt_time'])) == 0:
                results['task'] = self.create(task=postData['task'], date=postData['apt_date'], time=postData['apt_time'], user=currUser)
            else:
                results['errors'].append('That time is not available.')

        if len(results['errors']):
            results['status']=False
        
        return results

    

APPOINT_PENDING = 1
APPOINT_DONE = 2
APPOINT_MISSED = 3
APPOINT_STATUSES = (
    (APPOINT_PENDING, 'Pending'),
    (APPOINT_DONE, 'Done'),
    (APPOINT_MISSED, 'Missed'),
)

class Appointment(models.Model):
    task = models.CharField(max_length = 200)
    user = models.ForeignKey(User, related_name='tasks')
    status = models.IntegerField(choices=APPOINT_STATUSES, default=1)
    date = models.DateField()
    time = models.TimeField()
    objects = AppointManager()
