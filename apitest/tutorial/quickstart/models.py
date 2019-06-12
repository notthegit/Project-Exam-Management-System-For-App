from django.db import models

# Create your models here.
class Alert(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField()
    dashboard_id = models.BigIntegerField()
    panel_id = models.BigIntegerField()
    org_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    message = models.TextField()
    state = models.CharField(max_length=190)
    settings = models.TextField()
    frequency = models.BigIntegerField()
    handler = models.BigIntegerField()
    severity = models.TextField()
    silenced = models.IntegerField()
    execution_error = models.TextField()
    eval_data = models.TextField(blank=True, null=True)
    eval_date = models.DateTimeField(blank=True, null=True)
    new_state_date = models.DateTimeField()
    state_changes = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'alert'


class AlertNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    name = models.CharField(max_length=190)
    type = models.CharField(max_length=255)
    settings = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    is_default = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'alert_notification'
        unique_together = (('org_id', 'name'),)


class Annotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    alert_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    dashboard_id = models.BigIntegerField(blank=True, null=True)
    panel_id = models.BigIntegerField(blank=True, null=True)
    category_id = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=25)
    title = models.TextField()
    text = models.TextField()
    metric = models.CharField(max_length=255, blank=True, null=True)
    prev_state = models.CharField(max_length=25)
    new_state = models.CharField(max_length=25)
    data = models.TextField()
    epoch = models.BigIntegerField()
    region_id = models.BigIntegerField(blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'annotation'


class AnnotationTag(models.Model):
    annotation_id = models.BigIntegerField()
    tag_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'annotation_tag'
        unique_together = (('annotation_id', 'tag_id'),)


class ApiKey(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    name = models.CharField(max_length=190)
    key = models.CharField(unique=True, max_length=190)
    role = models.CharField(max_length=255)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_key'
        unique_together = (('org_id', 'name'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Dashboard(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.IntegerField()
    slug = models.CharField(max_length=189)
    title = models.CharField(max_length=189)
    data = models.TextField()
    org_id = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    updated_by = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    gnet_id = models.BigIntegerField(blank=True, null=True)
    plugin_id = models.CharField(max_length=189, blank=True, null=True)
    folder_id = models.BigIntegerField()
    is_folder = models.IntegerField()
    has_acl = models.IntegerField()
    uid = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dashboard'
        unique_together = (('org_id', 'folder_id', 'title'), ('org_id', 'uid'),)


class DashboardAcl(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    dashboard_id = models.BigIntegerField()
    user_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    permission = models.SmallIntegerField()
    role = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dashboard_acl'
        unique_together = (('dashboard_id', 'user_id'), ('dashboard_id', 'team_id'),)


class DashboardProvisioning(models.Model):
    id = models.BigAutoField(primary_key=True)
    dashboard_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=150)
    external_id = models.TextField()
    updated = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dashboard_provisioning'


class DashboardSnapshot(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    key = models.CharField(unique=True, max_length=190)
    delete_key = models.CharField(unique=True, max_length=190)
    org_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    external = models.IntegerField()
    external_url = models.CharField(max_length=255)
    dashboard = models.TextField()
    expires = models.DateTimeField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dashboard_snapshot'


class DashboardTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    dashboard_id = models.BigIntegerField()
    term = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dashboard_tag'


class DashboardVersion(models.Model):
    id = models.BigAutoField(primary_key=True)
    dashboard_id = models.BigIntegerField()
    parent_version = models.IntegerField()
    restored_from = models.IntegerField()
    version = models.IntegerField()
    created = models.DateTimeField()
    created_by = models.BigIntegerField()
    message = models.TextField()
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dashboard_version'
        unique_together = (('dashboard_id', 'version'),)


class DataSource(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    version = models.IntegerField()
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=190)
    access = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    database = models.CharField(max_length=255, blank=True, null=True)
    basic_auth = models.IntegerField()
    basic_auth_user = models.CharField(max_length=255, blank=True, null=True)
    basic_auth_password = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.IntegerField()
    json_data = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    with_credentials = models.IntegerField()
    secure_json_data = models.TextField(blank=True, null=True)
    read_only = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_source'
        unique_together = (('org_id', 'name'),)


class DatabaseManagementDateexam(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    date_exam = models.CharField(max_length=256)
    time_period = models.IntegerField()
    room_id = models.ForeignKey('DatabaseManagementRoom', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'database_management_dateexam'


class DatabaseManagementMajor(models.Model):
    major_name = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'database_management_major'


class DatabaseManagementProject(models.Model):
    proj_years = models.IntegerField()
    proj_semester = models.IntegerField()
    proj_name_th = models.CharField(max_length=1024)
    proj_name_en = models.CharField(max_length=1024)
    proj_major = models.CharField(max_length=1024)
    proj_advisor = models.CharField(max_length=1024)
    proj_co_advisor = models.CharField(max_length=1024)
    schedule_id = models.IntegerField(blank=True, null=True)
    sche_post_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'database_management_project'


class DatabaseManagementRoom(models.Model):
    room_name = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'database_management_room'


class DatabaseManagementScheduleposter(models.Model):
    date_post = models.CharField(max_length=256)
    proj_id = models.ForeignKey(DatabaseManagementProject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'database_management_scheduleposter'


class DatabaseManagementScheduleroom(models.Model):
    date_id = models.ForeignKey(DatabaseManagementDateexam, models.DO_NOTHING, blank=True, null=True)
    room_id = models.ForeignKey(DatabaseManagementRoom, models.DO_NOTHING)
    time_id = models.ForeignKey('DatabaseManagementTimeexam', models.DO_NOTHING, blank=True, null=True)
    proj_id = models.ForeignKey(DatabaseManagementProject, models.DO_NOTHING, blank=True, null=True)
    teacher_group = models.IntegerField()
    semester = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'database_management_scheduleroom'


class DatabaseManagementScoreadvisor(models.Model):
    proj_id = models.ForeignKey(DatabaseManagementProject, models.DO_NOTHING)
    propose = models.IntegerField()
    planning = models.IntegerField()
    tool = models.IntegerField()
    advice = models.IntegerField()
    improve = models.IntegerField()
    quality_report = models.IntegerField()
    quality_project = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'database_management_scoreadvisor'


class DatabaseManagementScoreposter(models.Model):
    proj_id = models.ForeignKey(DatabaseManagementProject, models.DO_NOTHING)
    time_spo = models.IntegerField()
    character_spo = models.IntegerField()
    presentation_spo = models.IntegerField()
    question_spo = models.IntegerField()
    media_spo = models.IntegerField()
    quality_spo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'database_management_scoreposter'


class DatabaseManagementScoreproj(models.Model):
    proj_id = models.ForeignKey(DatabaseManagementProject, models.DO_NOTHING)
    presentation = models.IntegerField()
    question = models.IntegerField()
    report = models.IntegerField()
    presentation_media = models.IntegerField()
    discover = models.IntegerField()
    analysis = models.IntegerField()
    quantity = models.IntegerField()
    levels = models.IntegerField()
    quality = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'database_management_scoreproj'


class DatabaseManagementSettings(models.Model):
    load = models.IntegerField()
    load_post = models.IntegerField()
    activate = models.IntegerField()
    forms = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'database_management_settings'


class DatabaseManagementStudent(models.Model):
    proj1_id = models.ForeignKey(DatabaseManagementProject, models.DO_NOTHING, blank=True, null=True)
    proj2_id = models.ForeignKey(DatabaseManagementProject, models.DO_NOTHING, blank=True, null=True)
    student_id = models.CharField(max_length=1024)
    student_name = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'database_management_student'


class DatabaseManagementTeacher(models.Model):
    teacher_name = models.CharField(max_length=1024)
    login_user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)
    measure_sproj = models.FloatField()
    measure_spost = models.FloatField()
    levels_teacher = models.FloatField()

    class Meta:
        managed = False
        db_table = 'database_management_teacher'


class DatabaseManagementTeacherMajorTeacher(models.Model):
    teacher = models.ForeignKey(DatabaseManagementTeacher, models.DO_NOTHING)
    major = models.ForeignKey(DatabaseManagementMajor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'database_management_teacher_major_teacher'
        unique_together = (('teacher', 'major'),)


class DatabaseManagementTeacherScheduleTeacher(models.Model):
    teacher = models.ForeignKey(DatabaseManagementTeacher, models.DO_NOTHING)
    scheduleroom = models.ForeignKey(DatabaseManagementScheduleroom, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'database_management_teacher_schedule_teacher'
        unique_together = (('teacher', 'scheduleroom'),)


class DatabaseManagementTeacherSchepostTeacher(models.Model):
    teacher = models.ForeignKey(DatabaseManagementTeacher, models.DO_NOTHING)
    scheduleposter = models.ForeignKey(DatabaseManagementScheduleposter, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'database_management_teacher_schepost_teacher'
        unique_together = (('teacher', 'scheduleposter'),)


class DatabaseManagementTeacherScoreAdvisor(models.Model):
    teacher = models.ForeignKey(DatabaseManagementTeacher, models.DO_NOTHING)
    scoreadvisor = models.ForeignKey(DatabaseManagementScoreadvisor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'database_management_teacher_score_advisor'
        unique_together = (('teacher', 'scoreadvisor'),)


class DatabaseManagementTeacherScorePosters(models.Model):
    teacher = models.ForeignKey(DatabaseManagementTeacher, models.DO_NOTHING)
    scoreposter = models.ForeignKey(DatabaseManagementScoreposter, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'database_management_teacher_score_posters'
        unique_together = (('teacher', 'scoreposter'),)


class DatabaseManagementTeacherScoreProjs(models.Model):
    teacher = models.ForeignKey(DatabaseManagementTeacher, models.DO_NOTHING)
    scoreproj = models.ForeignKey(DatabaseManagementScoreproj, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'database_management_teacher_score_projs'
        unique_together = (('teacher', 'scoreproj'),)


class DatabaseManagementTimeexam(models.Model):
    time_exam = models.CharField(max_length=256)
    time_period = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'database_management_timeexam'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LoginAttempt(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=190)
    ip_address = models.CharField(max_length=30)
    created = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'login_attempt'


class MigrationLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    migration_id = models.CharField(max_length=255)
    sql = models.TextField()
    success = models.IntegerField()
    error = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'migration_log'


class Org(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.IntegerField()
    name = models.CharField(unique=True, max_length=190)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    billing_email = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'org'


class OrgUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    role = models.CharField(max_length=20)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'org_user'
        unique_together = (('org_id', 'user_id'),)


class Playlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    interval = models.CharField(max_length=255)
    org_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'playlist'


class PlaylistItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    playlist_id = models.BigIntegerField()
    type = models.CharField(max_length=255)
    value = models.TextField()
    title = models.TextField()
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'playlist_item'


class PluginSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField(blank=True, null=True)
    plugin_id = models.CharField(max_length=190)
    enabled = models.IntegerField()
    pinned = models.IntegerField()
    json_data = models.TextField(blank=True, null=True)
    secure_json_data = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    plugin_version = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plugin_setting'
        unique_together = (('org_id', 'plugin_id'),)


class Preferences(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    version = models.IntegerField()
    home_dashboard_id = models.BigIntegerField()
    timezone = models.CharField(max_length=50)
    theme = models.CharField(max_length=20)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'preferences'


class Quota(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    target = models.CharField(max_length=190)
    limit = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'quota'
        unique_together = (('org_id', 'user_id', 'target'),)


class Session(models.Model):
    key = models.CharField(primary_key=True, max_length=16)
    data = models.TextField()
    expiry = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'session'


class Star(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    dashboard_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'star'
        unique_together = (('user_id', 'dashboard_id'),)


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tag'
        unique_together = (('key', 'value'),)


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=190)
    org_id = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    email = models.CharField(max_length=190, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'
        unique_together = (('org_id', 'name'),)


class TeamMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    team_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'team_member'
        unique_together = (('org_id', 'team_id', 'user_id'),)


class TempUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_id = models.BigIntegerField()
    version = models.IntegerField()
    email = models.CharField(max_length=190)
    name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=190)
    status = models.CharField(max_length=20)
    invited_by_user_id = models.BigIntegerField(blank=True, null=True)
    email_sent = models.IntegerField()
    email_sent_on = models.DateTimeField(blank=True, null=True)
    remote_addr = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'temp_user'


class TestData(models.Model):
    metric1 = models.CharField(max_length=20, blank=True, null=True)
    metric2 = models.CharField(max_length=150, blank=True, null=True)
    value_big_int = models.BigIntegerField(blank=True, null=True)
    value_double = models.FloatField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_int = models.IntegerField(blank=True, null=True)
    time_epoch = models.BigIntegerField()
    time_date_time = models.DateTimeField()
    time_time_stamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'test_data'


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.IntegerField()
    login = models.CharField(unique=True, max_length=190)
    email = models.CharField(unique=True, max_length=190)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    salt = models.CharField(max_length=50, blank=True, null=True)
    rands = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    org_id = models.BigIntegerField()
    is_admin = models.IntegerField()
    email_verified = models.IntegerField(blank=True, null=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    help_flags1 = models.BigIntegerField()
    last_seen_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserAuth(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    auth_module = models.CharField(max_length=190)
    auth_id = models.CharField(max_length=100)
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_auth'