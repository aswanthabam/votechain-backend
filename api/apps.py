# myapp/apps.py
from django.apps import AppConfig
from django.conf import settings

class FaceConfig(AppConfig):
    detector = None
    sp = None
    facerec = None
    FACE_THRESHOLD = 0.9
    name = 'api'

    def ready(self):
        if settings.DEBUG:
            print("Loading Face Verification Models")
            import dlib
            FaceConfig.detector = dlib.get_frontal_face_detector()
            FaceConfig.sp = dlib.shape_predictor("./assets/models/shape_predictor_68_face_landmarks.dat")
            FaceConfig.facerec = dlib.face_recognition_model_v1("./assets/models/dlib_face_recognition_resnet_model_v1.dat")
            FaceConfig.FACE_THRESHOLD = 0.9
    @staticmethod
    def get_face_embeddings(image_url) -> list | None:
        if not settings.DEBUG:return None
        import dlib
        import numpy as np
        image = dlib.load_rgb_image(image_url)
        faces = FaceConfig.detector(image)
        if len(faces) < 1:
            return None
        elif len(faces)> 1:
            print("More than one face")
            return None
        else:
            face = faces[0]
            shape = FaceConfig.sp(image, face)
            face_descriptor = FaceConfig.facerec.compute_face_descriptor(image, shape)
            face_embedding = np.array(face_descriptor)
            return face_embedding
    @staticmethod
    def verify_face(face1, face2) -> bool:
        from scipy.spatial.distance import cosine
        return (1 - cosine(face1, face2)) > FaceConfig.FACE_THRESHOLD