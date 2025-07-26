from django.contrib import admin
from .models import UploadedFile, StatusHistory

# Register your models here.

class StatusHistoryInline(admin.TabularInline):
    """
    Yeh inline view aapko UploadedFile ke admin page par hi uski saari status history dikhayega.
    Isse aapko alag se history page par jaane ki zaroorat nahi padegi.
    """
    model = StatusHistory
    # Dikhane waale fields
    fields = ('status', 'changed_at', 'changed_by')
    # In fields ko aap badal nahi sakte, yeh sirf dekhne ke liye hain.
    readonly_fields = ('status', 'changed_at', 'changed_by')
    # Nayi history add karne ka option yahan nahi hoga.
    extra = 0
    # Is inline ko delete karne ki permission nahi hogi.
    can_delete = False

    def has_add_permission(self, request, obj=None):
        # Admin se history add karne ki permission band kar rahe hain.
        return False


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    """
    UploadedFile model ke liye custom admin configuration.
    """
    # List view mein kaun se columns dikhenge.
    list_display = ('id', 'user', 'category', 'status', 'uploaded_at', 'file_link')
    
    # Kin-kin cheezon se list ko filter kar sakte hain.
    list_filter = ('status', 'category', 'uploaded_at')
    
    # Kin fields ke basis par search kar sakte hain.
    # user__username se aap સીધા user ke naam se search kar payenge.
    search_fields = ('category', 'user__username', 'id')
    
    # Detail view mein kaun se fields sirf padhne ke liye honge (non-editable).
    readonly_fields = ('user', 'uploaded_at', 'file_link_secure')
    
    # Detail view mein fields ko sections mein organize karna.
    fieldsets = (
        ('File Information', {
            'fields': ('user', 'category', 'file', 'file_link_secure')
        }),
        ('Status and Tracking', {
            'fields': ('status', 'uploaded_at')
        }),
    )
    
    # UploadedFile ke page par hi StatusHistory ko inline dikhana.
    inlines = [StatusHistoryInline]

    def file_link(self, obj):
        # File ka direct link provide karna (agar file hai toh).
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">View File</a>'
        return "No file"
    file_link.allow_tags = True
    file_link.short_description = 'Uploaded File'

    def file_link_secure(self, obj):
        # Yeh bhi file ka link hai, detail view ke liye.
        return self.file_link(obj)
    file_link_secure.allow_tags = True
    file_link_secure.short_description = 'Click to View File'


@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    """
    StatusHistory model ke liye admin configuration.
    Yeh alag se history dekhne ke liye hai.
    """
    list_display = ('file_id', 'status', 'changed_at', 'changed_by')
    search_fields = ('file__id', 'changed_by__username')
    
    def file_id(self, obj):
        # History list mein file ki ID dikhana.
        return obj.file.id
    file_id.short_description = 'File ID'
