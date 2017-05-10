from django.core.validators import RegexValidator

from rest_framework import serializers

from notgoogleplus.apps.accounts.serializers import AccountSerializer

from .models import Profile


ALPHABET = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    user = AccountSerializer(read_only=True, required=False)
    # username = serializers.CharField(source='user.username', required=False)
    first_name = serializers.CharField(required=False, allow_blank=True,
                                       validators=[ALPHABET], max_length=20)
    last_name = serializers.CharField(required=False, allow_blank=True,
                                      validators=[ALPHABET], max_length=20)
    nickname = serializers.CharField(required=False, allow_blank=True,
                                     validators=[ALPHABET], max_length=20)
    tagline = serializers.CharField(required=False, allow_blank=True, max_length=140)
    bio = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    dob = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(required=False, allow_blank=True, choices=GENDER_CHOICES)
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'nickname', 'tagline',
                  'bio', 'dob', 'gender', 'following', 'user',)
        # read_only_fields = ('username',)

    # def get_user(self, instance):
        # request = self.context.get('request')
        # if request.user == instance:
            # serializer = AccountSerializer(instance.user)
            # return serializer.data

    def get_following(self, instance):
        user = self.context.get('request').user
        followee = instance
        return instance.is_following(followee)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user')
        return queryset


class ProfileFollowSerializer(ProfileSerializer):
    follow = serializers.BooleanField(required=True, write_only=True)

    class Meta(ProfileSerializer.Meta):
        fields = ('username', 'first_name', 'last_name', 'nickname', 'tagline',
                  'bio', 'dob', 'gender', 'following', 'follow', 'user',)

    def validate(self, data):
        user = self.context.get('request').user
        followee = self.instance
        if data.get('follow') is True and user.profile == followee:
            raise serializers.ValidationError('You can not follow yourself.')
        if data.get('follow') != user.profile.is_following(followee):
            if data.get('follow'):
                user.profile.follow(followee)
            else:
                user.profile.unfollow(followee)

        return data

    # update function is overridden to stop the extra call to
    # save() function of ModelSerializer for the model instance
    def update(self, instance, validated_data):
        return instance


# class DynamicModelSerializer(serializers.ModelSerializer):
# """
# A ModelSerializer that takes an additional `fields` argument that
# controls which fields should be displayed, and takes in a "nested"
# argument to return nested serializers
# """

# def __init__(self, *args, **kwargs):
#     fields = kwargs.pop("fields", None)
#     exclude = kwargs.pop("exclude", None)
#     nest = kwargs.pop("nest", None)

    # if nest is not None and nest == True:
    #     self.Meta.depth = 1

#     super(DynamicModelSerializer, self).__init__(*args, **kwargs)

#     if fields is not None:
#         # Drop any fields that are not specified in the `fields` argument.
#         allowed = set(fields)
#         existing = set(self.fields.keys())
#         for field_name in existing - allowed:
#             self.fields.pop(field_name)

#     if exclude is not None:
#         for field_name in exclude:
#             self.fields.pop(field_name)
