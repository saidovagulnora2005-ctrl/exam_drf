from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', category_list_view),
    path('courses/', course_list_view),
    path('courses/<int:course_id>/', course_detail_view),  
    path('courses/<int:course_id>/buy/', buy_course_view),  
    path('my-courses/', my_courses_view),
    path('courses/<int:course_id>/lessons/', lesson_list_view),
    path('lessons/<int:lesson_id>/tasks/', task_list_view),
    path('courses/<int:course_id>/reviews/create/', create_review_view),

    path('author/courses/', author_courses_view),
    path('author/courses/create/', create_course_view),
    path('author/courses/<int:course_id>/update/', update_course_view),
    path('author/courses/<int:course_id>/delete/', delete_course_view),
    path('author/courses/<int:course_id>/lessons/create/', create_lesson_view),
    path('author/lessons/<int:lesson_id>/update/', update_lesson_view),
    path('author/lessons/<int:lesson_id>/delete/', delete_lesson_view),
    path('author/lessons/<int:lesson_id>/tasks/create/', create_task_view),
    path('author/tasks/<int:task_id>/update/', update_task_view),
    path('author/tasks/<int:task_id>/delete/', delete_task_view),
    
    path('admin/users/', admin_users_view),
    path('admin/users/<int:user_id>/delete/', admin_delete_user_view),
    path('admin/categories/create/', admin_create_category_view),
    path('admin/categories/<int:category_id>/update/', admin_update_category_view),
    path('admin/categories/<int:category_id>/delete/', admin_delete_category_view),
    path('admin/courses/', admin_courses_view),
]