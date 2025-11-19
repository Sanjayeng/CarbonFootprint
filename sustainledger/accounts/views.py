# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .forms import ProfileForm, UserUpdateForm
from .models import Notification, ActivityLog
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
import datetime



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # Pass request to AuthenticationForm so it can use request-related auth backends
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # redirect to next if present, else to home
            next_url = request.GET.get('next') or request.POST.get('next') or '/'
            return redirect(next_url)
        else:
            # Invalid credentials — show a message and re-render the form
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'login.html', {'form': form})
    else:
        # GET: show empty form (pass `request` for consistency)
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")


@login_required
def profile_view(request):
    return render(request, "profile.html")


@login_required
def profile_update(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("accounts:profile")
    return redirect("accounts:profile")




@login_required
def dashboard_view(request):
    # sample chart data: registrations last 7 days (example)
    today = timezone.now().date()
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    labels = [d.strftime("%b %d") for d in dates]

    # sample: count new users per day (replace with meaningful metrics)
    counts = []
    for d in dates:
        start = timezone.make_aware(datetime.datetime.combine(d, datetime.time.min))
        end = timezone.make_aware(datetime.datetime.combine(d, datetime.time.max))
        counts.append(User.objects.filter(date_joined__range=(start, end)).count())

    # quick stats for dashboard cards
    stats = {
        "total_users": User.objects.count(),
        "unread_notifications": request.user.notifications.filter(is_read=False).count(),
        "recent_activity": request.user.activities.all()[:7],
    }

    return render(request, "dashboard.html", {"labels": labels, "data": counts, "stats": stats})

# Chart data API (if you prefer loading via AJAX)
@login_required
def dashboard_data_api(request):
    # Example: return JSON for Chart.js (modify to real metrics)
    import datetime
    today = timezone.now().date()
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    labels = [d.strftime("%b %d") for d in dates]

    counts = []
    for d in dates:
        start = datetime.datetime.combine(d, datetime.time.min).replace(tzinfo=timezone.utc)
        end = datetime.datetime.combine(d, datetime.time.max).replace(tzinfo=timezone.utc)
        counts.append(User.objects.filter(date_joined__range=(start, end)).count())

    return JsonResponse({"labels": labels, "data": counts})

@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        uform = UserUpdateForm(request.POST, instance=user)
        pform = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            ActivityLog.objects.create(user=user, action="Updated profile")
            messages.success(request, "Profile updated")
            return redirect("accounts:profile")
    else:
        uform = UserUpdateForm(instance=user)
        pform = ProfileForm(instance=user.profile)
    return render(request, "profile.html", {"uform": uform, "pform": pform})

@login_required
def notifications_list(request):
    notifs = request.user.notifications.all().order_by("-created_at")
    return render(request, "notifications.html", {"notifications": notifs})

@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect("accounts:notifications")

@login_required
def activity_log(request):
    logs = request.user.activities.all()
    return render(request, "activity_log.html", {"logs": logs})

# Admin-only dashboard
def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def admin_dashboard(request):
    # some admin metrics
    total_users = User.objects.count()
    total_notifications = Notification.objects.count()
    total_activities = ActivityLog.objects.count()

    # recent users
    recent_users = User.objects.order_by("-date_joined")[:10]

    return render(request, "admin_dashboard.html", {
        "total_users": total_users,
        "total_notifications": total_notifications,
        "total_activities": total_activities,
        "recent_users": recent_users
    })

def unread_notifications_count(request):
    if request.user.is_authenticated:
        try:
            cnt = request.user.notifications.filter(is_read=False).count()
        except Exception:
            cnt = 0
        return {"unread_notifications_count": cnt}

    return {"unread_notifications_count": 0}

