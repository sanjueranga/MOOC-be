# Generated by Django 4.2.10 on 2024-06-03 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=255)),
                ('template_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('introduction', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CodingAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('description', models.TextField(blank=True, null=True)),
                ('deadline', models.DateTimeField()),
                ('points', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('approved', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('duration', models.CharField(max_length=255)),
                ('header_img', models.URLField(blank=True, null=True)),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('tags', models.TextField(blank=True, null=True)),
                ('course_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('offered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofiles.institution')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('deadline', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(choices=[('teacher', 'Teacher'), ('course-creator', 'Course Creator'), ('non-editing-teacher', 'Non-editing Teacher')], default='teacher', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('duration', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('introduction', models.CharField(max_length=255)),
                ('week_number', models.IntegerField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='VideoProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.enrollment')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.video')),
            ],
        ),
        migrations.CreateModel(
            name='QuizProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, null=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.enrollment')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('points', models.IntegerField(default=1)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.enrollment')),
            ],
        ),
        migrations.CreateModel(
            name='NotesProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.enrollment')),
                ('notes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.notes')),
            ],
        ),
        migrations.CreateModel(
            name='CourseTeachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.role')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoursePermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.CharField(choices=[('all', 'All'), ('teacher', 'Teacher'), ('course-creator', 'Course Creator')], default='course-creator', max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.permission')),
            ],
        ),
        migrations.CreateModel(
            name='CodingAssignmentProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.codingassignment')),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.enrollment')),
            ],
        ),
        migrations.CreateModel(
            name='ChapterContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.chapter')),
                ('coding_assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.codingassignment')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.notes')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.quiz')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.video')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='coding_assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.codingassignment'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.quiz'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.week'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_link', models.URLField()),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateTimeField()),
                ('certificate_number', models.CharField(max_length=255)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.enrollment')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='courses.question')),
            ],
        ),
    ]
