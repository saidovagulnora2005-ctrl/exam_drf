from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404



def is_author(user):
    return user.role == 'author'


def is_admin(user):
    return user.role == 'admin'


@api_view(['GET'])
@permission_classes([AllowAny])
def course_list_view(request):
    courses = Course.objects.filter(is_published=True)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def course_detail_view(request, course_id):
    course = get_object_or_404(Course,id=course_id,is_published=True)
    serializer = CourseSerializer(course)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([AllowAny])
def category_list_view(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_course_view(request, course_id):
    course = get_object_or_404(Course,id=course_id,is_published=True)
    if Purchase.objects.filter(user=request.user,course=course,status='Completed').exists():
        return Response({'error': 'Вы уже купили этот курс'},status=400)
    if Purchase.objects.filter(user=request.user,course=course,status='Pending').exists():
        return Response({'message': 'Покупка ожидает подтверждения'},status=200)
    purchase = Purchase.objects.create(user=request.user,
        course=course,amount=course.price,status='Pending')
    serializer = PurchaseSerializer(purchase)
    return Response(serializer.data, status=201)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses_view(request):
    purchases = Purchase.objects.filter(user=request.user,status='Completed')
    course_ids = purchases.values_list('course_id', flat=True)
    courses = Course.objects.filter(id__in=course_ids)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lesson_list_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    tasks = Task.objects.filter(lesson=lesson)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.role != 'student':
        return Response({'error': 'Только студенты могут оставлять отзывы'},status=403)
    if not Purchase.objects.filter(
        user=request.user,
        course=course,
        status='Completed').exists():
        return Response({'error': 'Сначала купите курс'},status=403)
    rating = request.data.get('rating')
    comment = request.data.get('comment')
    try:
        rating = int(rating)
    except (ValueError, TypeError):return Response({'error': 'Оценка должна быть числом'},status=400)
    if rating < 1 or rating > 5:
        return Response({'error': 'Оценка должна быть от 1 до 5'},status=400)
    review = Review.objects.create(course=course,user=request.user,rating=rating,comment=comment)
    serializer = ReviewSerializer(review)
    return Response(serializer.data, status=201)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def author_courses_view(request):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    courses = Course.objects.filter(author=request.user)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course_view(request):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_course_view(request, course_id):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    course = get_object_or_404(Course,id=course_id,author=request.user)
    data = request.data.copy()
    data.pop('author', None)
    serializer = CourseSerializer(course,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_course_view(request, course_id):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    course = get_object_or_404(Course,id=course_id,author=request.user)
    course.delete()
    return Response({'message': 'Курс удалён'}, status=200)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lesson_view(request, course_id):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    course = get_object_or_404(Course,id=course_id,author=request.user)
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(course=course)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_lesson_view(request, lesson_id):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    lesson = get_object_or_404(Lesson,id=lesson_id,course__author=request.user)
    data = request.data.copy()
    data.pop('course', None)
    serializer = LessonSerializer(lesson,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lesson_view(request, lesson_id):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    lesson = get_object_or_404(Lesson,id=lesson_id,course__author=request.user)
    lesson.delete()
    return Response({'message': 'Урок удалён'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task_view(request, lesson_id):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    lesson = get_object_or_404(Lesson,id=lesson_id,course__author=request.user)
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(lesson=lesson)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_task_view(request, task_id):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    task = get_object_or_404(Task,id=task_id,lesson__course__author=request.user)
    data = request.data.copy()
    data.pop('lesson', None)
    serializer = TaskSerializer(task,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task_view(request, task_id):
    if not is_author(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    task = get_object_or_404(Task,id=task_id,lesson__course__author=request.user)
    task.delete()
    return Response({'message': 'Задание удалено'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users_view(request):
    if not is_admin(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_user_view(request, user_id):
    if not is_admin(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    user = get_object_or_404(CustomUser, id=user_id)
    if user.id == request.user.id:
        return Response({'error': 'Нельзя удалить себя'}, status=400)
    user.delete()
    return Response({'message': 'Пользователь удалён'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_category_view(request):
    if not is_admin(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def admin_update_category_view(request, category_id):
    if not is_admin(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    category = get_object_or_404(Category, id=category_id)
    serializer = CategorySerializer(category,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_category_view(request, category_id):
    if not is_admin(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return Response({'message': 'Категория удалена'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_courses_view(request):
    if not is_admin(request.user):
        return Response({'error': 'Нет доступа'}, status=403)
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

