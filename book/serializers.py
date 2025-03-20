from rest_framework import serializers

from book import models


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Genre
        fields = ["id", "name"]


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Author
        fields = ["id", "first_name", "last_name"]


class AuthorListSerializer(AuthorSerializer):

    class Meta:
        model = models.Author
        fields = ["first_name", "last_name"]


class AuthorDetailSerializer(AuthorSerializer):

    class Meta:
        model = models.Author
        fields = ["id", "picture", "first_name", "last_name"]


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Chapter
        fields = ["id", "name", "book", "serial_number"]


class ChapterListSerializer(ChapterSerializer):

    class Meta:
        model = models.Chapter
        fields = ["id", "name", "serial_number"]


class ChapterDetailSerializer(ChapterSerializer):
    related_chapters = serializers.SerializerMethodField()

    class Meta:
        model = models.Chapter
        fields = ["id", "name", "serial_number", "file", "related_chapters"]

    def get_related_chapters(
            self,
            chapter: models.Chapter
    ) -> dict[str, int | None]:
        current_serial_number = chapter.serial_number
        book_id = chapter.book

        previous_chapter_id = self._get_chapter(
            book_id=book_id,
            serial_number=current_serial_number - 1
        )
        next_chapter_id = self._get_chapter(
            book_id=book_id,
            serial_number=current_serial_number + 1
        )

        return {
            "previous_chapter_id": previous_chapter_id,
            "next_chapter_id": next_chapter_id,
        }

    def _get_chapter(self, book_id: int, serial_number: int) -> int | None:
        chapter = models.Chapter.objects.filter(
            book=book_id,
            serial_number=serial_number
        ).first()

        if chapter:
            return chapter.id
        return None


class CommentarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Commentary
        fields = ["id", "book", "author", "content", "date", "parent"]

    def validate(self, attrs):
        if not (len(attrs) == 1 and attrs.get("content")):
            raise serializers.ValidationError(
                "Some unnecessary data were provided"
            )
        return super().validate(attrs)


class CommentaryCreateSerializer(CommentarySerializer):

    class Meta:
        model = models.Commentary
        fields = ["content", ]

    def create(self, validated_data):
        print(validated_data)
        validated_data["book"] = self.context["book"]
        validated_data["author"] = self.context["author"]
        print(validated_data)

        return super().create(validated_data)


class ReplyCreateSerializer(CommentarySerializer):

    class Meta:
        model = models.Commentary
        fields = ["content", ]

    def create(self, validated_data):
        parent = self.context["parent"]

        replying_to = str(parent.author)
        validated_data["content"] = (
            replying_to + ", " + validated_data["content"]
        )

        if parent.parent:
            print("in if statement")
            parent = parent.parent

        validated_data["parent"] = parent
        validated_data["author"] = self.context["author"]
        return super().create(validated_data)


class CommentDetailSerializer(CommentarySerializer):
    author = AuthorListSerializer(read_only=True)


class ReplyBookDetailSerializer(CommentDetailSerializer):

    class Meta:
        model = models.Commentary
        fields = ["id", "author", "content", "date"]


class CommentaryBookDetailSerializer(CommentDetailSerializer):
    replies = ReplyBookDetailSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.Commentary
        fields = ["id", "author", "content", "date", "replies"]


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields = [
            "id",
            "image",
            "name",
            "genres",
            "authors",
            "pages",
            "summary",
        ]


class BookListSerializer(BookSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    authors = AuthorListSerializer(
        many=True,
        read_only=True,
    )


class BookDetailSerializer(BookListSerializer):
    chapters = ChapterListSerializer(
        many=True,
        read_only=True,
    )
    commentaries = CommentaryBookDetailSerializer(
        many=True,
        read_only=True
    )
    views = serializers.IntegerField()
    likes = serializers.IntegerField()
    authors = AuthorDetailSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = models.Book
        fields = [
            "id",
            "image",
            "name",
            "genres",
            "authors",
            "pages",
            "summary",
            "chapters",
            "commentaries",
            "views",
            "likes",
        ]
