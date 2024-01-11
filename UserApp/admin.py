import os
from django.contrib import admin
from django.http import HttpResponseRedirect
from . import models
from django.conf import settings
from . import action_static
import mammoth
from django.core.files import File
# Custom ModelAdmin class
class MyModelAdmin(admin.ModelAdmin):
    # ... other ModelAdmin options
    def save_model(self, request, obj, form, change):
        try:
            if request.method == 'POST':
                # Perform custom actions before saving
                # Get the path to the Resources folder
                resources_path = os.path.join(settings.BASE_DIR, 'UserApp', 'Resources')  # Assuming UserApp is in the project root
                with open('/path/to/your/file.txt', 'rb') as file:
                    file_contents = file.read()
                django_file = File(file_contents, name='file.txt')
                form['richtext'] = mammoth.convert_to_html()
                # Call the parent save_model method to persist changes
                super().save_model(request, obj, form, change)
                
        except Exception as e:  # Catch any saving-related errors
            self.message_user(request, f"Failed to save model: {e}")
            return HttpResponseRedirect(request.path)  # Stay on the same page

# Register your models here.
admin.site.register(models.Documentary)
    
admin.site.register(models.DocumentarySector)
admin.site.register(models.Quiz)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.UserDocumentary)
admin.site.register(models.UserDocumentSection)
admin.site.register(models.UserQuiz)
admin.site.register(models.tmp_UserQuizQuestionAnswer)
admin.site.register(models.tmp_UQ_QuestionUser)
admin.site.register(models.UserInfo)