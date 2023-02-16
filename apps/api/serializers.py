from django.contrib.auth import get_user_model
from django.db.models.fields import CharField
from rest_framework import fields, response, serializers
from drf_extra_fields.fields import Base64ImageField
from apps.user import models as user_mds
from apps.blog import models as blog_mds
from apps.tour import models as tour_mds
from apps.system import models as system_mds
from djoser.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.serializers import UserCreateSerializer as BaseCreateUserSerializer

User = get_user_model()  
username_field = User.USERNAME_FIELD if hasattr(User, 'USERNAME_FIELD') else 'username'


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")

    class Meta:
        model = settings.TOKEN_MODEL
        fields = ("auth_token")
        #depth = 1


class CustomerUserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_mds.CustomerType
        fields = ['id','type_name','status']
        read_only_fields = ['id','type_name','status']


class CustomerUserProfileSerializer(serializers.ModelSerializer):
    #customer_type = CustomerUserTypeSerializer()
    class Meta:
        model = user_mds.CustomerUserProfile
        fields = ['id','user','is_customer','customer_type']
        read_only_fields = ('user','is_customer')


class UserSerializer(serializers.ModelSerializer):
    customer_user_profile = CustomerUserProfileSerializer(required = True)  #serializers.ReadOnlyField(source = 'user.customeruser.is_customer')
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            "id",
            "username",
            "image",
            'first_name',
            'last_name',
            'phone_number',
            'customer_user_profile'
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        customer_data = validated_data.pop('customer_user_profile',None)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        if customer_data is not None:
            instance.customer_user_profile.customer_type = customer_data['customer_type']
            instance.customer_user_profile.save(update_fields=["customer_type"])
        return super().update(instance, validated_data)

    
""" class UserCreateSerializer(BaseCreateUserSerializer):
    customer_user_profile = CustomerUserProfileSerializer(required = True)
    class Meta(BaseCreateUserSerializer.Meta):
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "customer_user_profile",
            "password"
        )
    def updatep(self, instance, validated_data):
        data = validated_data.pop('customer_user_profile')
        profile = instance.customer_user_profile
        profile.customer_type = data.get('customer_type',profile.customer_type)
        profile.save()

    def validate(self, attrs):
        #data = attrs.pop('customer_user_profile')
        user = User(**attrs)
       
        password = attrs.get("password")
       # attrs.get("customer_user_profile")
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )
        return attrs

    def create(self, validated_data):
        print("CUSTOMER SERIALIZER RUNNING")       
        try:    
            #customer_data = validated_data.pop('customer_user_profile',None)      
            user = self.perform_create(validated_data) 
            self.updatep(user,validated_data)
            #profile = user.customer_user_profile
            #print(f'user profile: {profile}')
            #profile.customer_type = customer_data.get('customer_type',profile.customer_type)
            #profile.save()


            #profile = mds.CustomerUserProfile.objects.get_or_create(user=user)
            #if profile:
                #profile.customer_type = customer_data['customer_type']
                #profile.customer_user_profile.save()
            #self.fields.pop('customer_user_profile')
            #mds.CustomerUserProfile.objects.create(user=user, **d)         
        except IntegrityError:
            self.fail("cannot_create_user")
        return user


    def perform_create(self, validated_data):
        print("customer created")
        with transaction.atomic():
            customer_data = validated_data.pop('customer_user_profile',None)
            user = User.objects.create_user(**validated_data)
            
           
            
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user """


""" class UserCreatePasswordRetypeSerializer(UserCreateSerializer):
    default_error_messages = {
        "password_mismatch": settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
       # attrs.pop("customer_user_profile")
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch") """


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
       model = system_mds.ContactMessage
       fields = ["full_name","email_address","text_message"]
       read_only_fields = ["id"]


class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
       model = system_mds.NewsletterSubscription
       fields = ["full_name","email_address"]
       write_only_fields = ("full_name","email_address")


class CompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = system_mds.CompanyImage
        fields = ['image']


class AdminUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = user_mds.AdminUserProfile
        fields = ['user','is_admin']


class CompanyAdminSerializer(serializers.ModelSerializer):
    #image = serializers.ReadOnlyField(source = 'user.user.image',read_only = True)
    #first_name = serializers.CharField(source = 'user.user') #UserSerializer() #serializers.CharField(source = 'user.user__first_name', read_only=True)
    admin_profile =  AdminUserSerializer(read_only = True,source='user') #CustomerSerializer(read_only=True)
    class Meta:
        model = system_mds.CompanyAdmin
        fields = ['admin_profile','title']
        #depth = 2


class CompanyStatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = system_mds.CompanyStatement
        fields = ['image','statement_title','statement']


class CompanySocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = system_mds.SocialMedia
        fields = ['social_media_icon','social_media_handle']


class AppSettingSerializer(serializers.ModelSerializer):
    company_images = CompanyImageSerializer(many=True,read_only=True)
    company_admins = CompanyAdminSerializer(many=True,read_only=True)
    company_statements = CompanyStatmentSerializer(many=True,read_only=True)
    company_social_medias = CompanySocialMediaSerializer(many=True,read_only=True)
    class Meta:
       model = system_mds.Settings
       fields = ('id','company_name','description','meta_title','meta_description',
                'meta_keywords','logo','icon','address_code','email','email_message',
                'phone_number','phone_message','fax','physical_address',
                'physical_address_message','employee_number','launch_time',
                'tour_bookings','status','company_images','company_admins',
                'company_statements','company_social_medias'
            )
    

class ReviewTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_mds.TourReview
        fields = ['tour','customer','rating','review']


class ToursReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_mds.TourReview
        fields = '__all__'


class TourReviewSerializer(serializers.ModelSerializer):
    customer_first_name = serializers.ReadOnlyField(source = 'customer.user.first_name')
    customer_last_name = serializers.ReadOnlyField(source = 'customer.user.last_name')
    customer_type = serializers.ReadOnlyField(source = 'customer.customer_user_profile.customer_type')
    customer_image = serializers.ImageField(source = 'customer.user.image')
    tour = serializers.ReadOnlyField(source = 'tour.tour_slug')
    class Meta:
        model = tour_mds.TourReview
        fields = ['customer_first_name','customer_last_name','customer_type','customer_image','tour','rating','review','review_date','status']
        #depth = 


class RelatedTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_mds.RelatedTour
        fields = ['related_tour']
        depth = 1
       
    
class TourImageSerializer(serializers.ModelSerializer):
    #imageName = Base64ImageField(required=False)
    class Meta:
        model = tour_mds.TourImage
        fields = '__all__'
        

class TourTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_mds.TourTag
        fields = '__all__'
       

class TourQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_mds.TourQuestion
        fields = '__all__'
        

class TourProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_mds.TourProgram
        fields = '__all__'
        

class TourInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_mds.TourInclusion
        fields = '__all__'
       

class TourInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_mds.TourInsight
        fields = '__all__'


class ToursSerializer(serializers.ModelSerializer):
    #tour_reviews = ToursReviewSerializer(many= True,read_only=True)
    #num_reviews = serializers.IntegerField(read_only = True)
    class Meta:
        model = tour_mds.Tour
        lookup_field = 'tour_slug'
        fields = (
            'id','tour_slug','name','destination','category','image',
            'description','advertise','ad_title','ad_name','ad_description',
            'price','discount','discounted_price','duration','new_tag','reviews',
            'rating','added','status'
        )
        

class TourSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    destination = serializers.ReadOnlyField(source='destination.name')
    destination_country = serializers.ReadOnlyField(source='destination.country')
    related_tours = RelatedTourSerializer(many=True,read_only=True)
    tour_tags = TourTagSerializer(many=True,read_only=True)
    tour_images = TourImageSerializer(many=True,read_only=True)
    tour_questions = TourQuestionSerializer(many=True,read_only=True)
    tour_programs = TourProgramSerializer(many=True,read_only=True)
    tour_inclusions = TourInclusionSerializer(many=True,read_only=True)
    tour_insights = TourInsightSerializer(many=True,read_only=True)
    class Meta:
        model = tour_mds.Tour
        lookup_field = 'tour_slug'
        read_only_fields =('id','tour_slug','rating')
        fields = (
            'id','tour_slug','name','destination_country','destination',
            'category','image','description','advertise','ad_title','ad_name',
            'ad_description','price','discount','discounted_price','duration',
            'new_tag','reviews','rating','added','status','related_tours',
            'tour_tags','tour_images','tour_questions','tour_programs',
            'tour_inclusions','tour_insights'
            )


class TourDestinationSerializer(serializers.ModelSerializer):
    #destinations = serializers.HyperlinkedIdentityField(view_name="destinations",format='html')
    num_tours = serializers.IntegerField(read_only = True)
    class Meta:
        model = tour_mds.TourDestination
        fields = ('id','destination_slug','name','image','tag_line','tag_text',
        'description','num_tours','status')
        lookup_field = 'destination_slug'


class TourCategorySerializer(serializers.ModelSerializer):
    num_tours = serializers.IntegerField(read_only = True)
    class Meta:
        model = tour_mds.TourCategory
        fields = ('id','category_slug','name','image','description','num_tours','status')
        lookup_field = 'category_slug'










        """ fields = ('id','tourName','description','price','discount',
            'duration','status','destination','category','related','tags',
            'images','questions','programs','inclusions','insights') """

    """ def create(self,validated_data):
        relateds_data = validated_data.pop('related')
        tags_data = validated_data.pop('tags')
        images_data = validated_data.pop('images')
        questions_data = validated_data.pop('questions')
        programs_data = validated_data.pop('programs')
        inclusions_data = validated_data.pop('inclusions')
        insights_data = validated_data.pop('insights')

        tour_obj = mds.Tour.objects.create(**validated_data)
        for related_data in relateds_data:
            mds.RelatedTour.objects.create(tour=tour_obj,**related_data)

        for tag_data in tags_data:
            mds.TourTag.objects.create(tour=tour_obj,**tag_data) 

        for image_data in images_data:
            mds.TourImage.objects.create(tour=tour_obj,**image_data)

        for question_data in questions_data:
            mds.TourQuestion.objects.create(tour=tour_obj,**question_data)

        for program_data in programs_data:
            mds.TourProgram.objects.create(tour=tour_obj,**program_data)

        for inclusion_data in inclusions_data:
            mds.TourInclusion.objects.create(tour=tour_obj,**inclusion_data)

        for insight_data in insights_data:
            mds.TourInsight.objects.create(tour=tour_obj,**insight_data)

        return tour_obj """

    """ def update(self,instance,validated_data):
        relateds_data = validated_data.pop('related')
        tags_data = validated_data.pop('tags')
        images_data = validated_data.pop('images')
        questions_data = validated_data.pop('questions')
        programs_data = validated_data.pop('programs')
        inclusions_data = validated_data.pop('inclusions')
        insights_data = validated_data.pop('insights')



        relateds = (instance.related).all()
        relateds = list(relateds)

        tags = (instance.tags).all()
        tags = list(tags)

        images = (instance.images).all()
        images = list(images)

        questions = (instance.questions).all()
        questions = list(questions)

        programs = (instance.programs).all()
        programs = list(programs)

        inclusions = (instance.inclusions).all()
        inclusions = list(inclusions)

        insights = (instance.insights).all()
        insights = list(insights)


        instance.tourName = validated_data.get('tourName',instance.tourName)
        instance.description = validated_data.get('description',instance.description)
        instance.price = validated_data.get('price',instance.price)
        instance.discount = validated_data.get('discount',instance.discount)
        instance.duration = validated_data.get('duration',instance.duration)
        instance.status = validated_data.get('status',instance.status)
        instance.destination = validated_data.get('destination',instance.destination)
        instance.category = validated_data.get('category',instance.category)
        instance.save()

        for related_data in relateds_data:
            related = relateds.pop(0)
            related.id = related_data.get('id',related.id)
            related.tour = related_data.get('tour',related.tour)
            related.save()

        for tag_data in tags_data:
            tag = tags.pop(0)
            tag.id = tag_data.get('id',tag.id)
            tag.tour = tag_data.get('tour',tag.tour)
            tag.tagName = tag_data.get('tagName',tag.tagName)
            tag.save()

        for image_data in images_data:
            image = images.pop(0)
            image.id = image_data.get('id',tag.id)
            image.tour = image_data.get('tour',image.tour)
            image.imageName = image_data.get('imageName',image.imageName)
            image.save()

        for question_data in questions_data:
            question = questions.pop(0)
            question.id = question_data.get('id',question.id)
            question.tour = question_data.get('tour',question.tour)
            question.question = question_data.get('question',question.question)
            question.answer = question_data.get('answer',question.answer)
            question.save()

        for program_data in programs_data:
            program = programs.pop(0)
            program.id = program_data.get('id',program.id)
            program.tour = program_data.get('tour',program.tour)
            program.programName = program_data.get('programName',program.programName)
            program.programDuration = program_data.get('programDuration',program.programDuration)
            program.programDesc = program_data.get('programDesc',program.programDesc)
            program.programName = program_data.get('programName',program.programName)
            program.save()

        for inclusion_data in inclusions_data:
            inclusion = inclusions.pop(0)
            inclusion.id = inclusion_data.get('id',inclusion.id)
            inclusion.tour = inclusion_data.get('tour',inclusion.tour)
            inclusion.inclusionName = inclusion_data.get('inclusionName',inclusion.inclusionName)
            inclusion.inclusionDesc = inclusion_data.get('inclusionDesc',inclusion.inclusionDesc)
            inclusion.save()

        for insight_data in insights_data:
            insight = insights.pop(0)
            insight.id = insight_data.get('id',insight.id)
            insight.tour = insight_data.get('tour',insight.tour)
            insight.insightName = insight_data.get('insightName',insight.insightName)
            insight.insightDesc = insight_data.get('insightDesc',insight.insightDesc)
            insight.save()

        return instance """


class BlogArticleSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source = 'category.name')
    class Meta:
        model = blog_mds.BlogArticle
        read_only_fields = ['id','article_slug','publish_date','status']
        fields = ('id','article_slug','article_title','category','image','article_intro','article','publish_date','status')
        lookup_field = 'article_slug'


class BlogCategorySerializer(serializers.HyperlinkedModelSerializer):
    blogarticlemodel_set = BlogArticleSerializer(many=True,read_only = True)
    class Meta:
        model = blog_mds.BlogCategory
        fields = ('id','blog_category_slug','name','blogarticlemodel_set','image','description','status')
        lookup_field ='blog_category_slug'


class TourBookSerialiazer(serializers.ModelSerializer):
    class Meta: 
        model = tour_mds.TourBooking
        fields = ('id','tour','customer','booking_date','arrival_date','tour_start_date','pickup_address','dropoff_address','adults','children','extra_info')
        read_only_fields = ('id',)


class TourBookingSerialiazer(serializers.ModelSerializer):
    tour = serializers.ReadOnlyField(source='tour.name')
    class Meta: 
        model = tour_mds.TourBooking
        fields = ('id','tour','customer','booking_date','arrival_date','tour_start_date','pickup_address','dropoff_address','adults','children','extra_info')
        read_only_fields = ('id','tour','customer','booking_date','arrival_date','tour_start_date','pickup_address','dropoff_address','adults','children','extra_info')


class TourBookingsSerialiazer(serializers.ModelSerializer):
    tour = serializers.ReadOnlyField(source='tour.name')
    class Meta: 
        model = tour_mds.TourBooking
        fields = ('id','tour','booking_date','arrival_date','tour_start_date','status')
        read_only_fields = ['id','tour','booking_date','status']
      