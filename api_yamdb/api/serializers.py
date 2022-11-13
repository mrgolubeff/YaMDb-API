from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .validators import validate_email, validate_username


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])
    username = serializers.CharField(validators=[validate_username])

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])
    username = serializers.CharField(validators=[validate_username])

    class Meta:
        model = User
        fields = ("email", "username")


class UserCheckSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=512)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        title_id = self.context["request"].parser_context["kwargs"]["title_id"]
        title = get_object_or_404(Title, pk=title_id)
        user = self.context["request"].user
        if (
            self.context["request"].method == "POST"
            and Review.objects.filter(author=user, title=title).exists()
        ):
            raise serializers.ValidationError(
                "Вы уже писали отзыв на это произведение!"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = ("name", "slug")
        exclude = ('id',)
        model = Genre
        lookup_field = "slug"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # fields = ("name", "slug")
        exclude = ('id',)
        model = Category
        lookup_field = "slug"


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Title


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category"
        )

    def validate_year(self, value):
        year_today = timezone.date.today().year
        if value > year_today:
            raise serializers.ValidationError(
                "Год создания произведения указан неверно!"
            )
        return value
