import dlib
import numpy as np
import cv2
from scipy.spatial.distance import cosine

class FaceEmbedding:

    VARIENCE_THREASHOLD = 0.0005
    
    def __init__(self) -> None:
        self.embedding = []
        self.embeddings = []
        # self.all_embeddings = []
        # self.varient_embeddings = []
        # self.varient_embeddings_count = 0
        self.valid_embeddings_count = 0
        self.added_embeddings_count = 0

    def __init__(self,embeddings:list[list],embedding:list) -> None:
        self.embedding = embedding
        self.embeddings = embeddings
        self.valid_embeddings_count = len(embeddings)
        self.added_embeddings_count = len(embeddings)

    def is_consistent(self,embedding1, embedding2) -> tuple[bool, float]:
        np_array = np.array([embedding1,embedding2])
        varience_dim = np.var(np_array,axis=0)
        mean_varience = np.mean(varience_dim)
        return (mean_varience < self.VARIENCE_THREASHOLD and mean_varience > -self.VARIENCE_THREASHOLD, mean_varience, )
    
    def add_embeddings(self,embedding) -> bool:
        # self.all_embeddings.append(embedding)
        self.added_embeddings_count += 1
        if self.valid_embeddings_count == 0:
            print(" # Adding initial embedding .")
            self.embeddings.append(embedding)
            self.embedding = embedding
            self.valid_embeddings_count = 1
            return True
        else:
            print(" # Adding additional embedding " )
            consistency = self.is_consistent(self.embedding, embedding)
            if consistency[0]:
                print(f" # Embedding is consistent ({consistency[1]})" )
                self.embeddings.append(embedding)
                np_embeddings = np.array(self.embeddings)
                self.embedding = np.mean(np_embeddings, axis=0).tolist() # update the embedding
                return True
            else:
                print(f" # Embedding is not consistent ({consistency[1]})" )
                # self.varient_embeddings.append(embedding)
                return False

class FaceVerifier:

    THREASHOLD = 0.95
    sp = dlib.shape_predictor("assets/models/shape_predictor_68_face_landmarks.dat")
    facerec = dlib.face_recognition_model_v1("assets/models/dlib_face_recognition_resnet_model_v1.dat")
    face_cascade = cv2.CascadeClassifier('assets/models/haarcascade_frontalface_default.xml')

    def __init__(self):
        self.sp = dlib.shape_predictor("assets/models/shape_predictor_68_face_landmarks.dat")
        self.facerec = dlib.face_recognition_model_v1("assets/models/dlib_face_recognition_resnet_model_v1.dat")
        self.face_cascade = cv2.CascadeClassifier('assets/models/haarcascade_frontalface_default.xml')
    
    @staticmethod
    def verify_face(face1, face2) -> bool:
        similarity = 1 - cosine(face1, face2)
        return (similarity > FaceVerifier.THREASHOLD, FaceVerifier.calculate_percentage(similarity),similarity)
    
    @staticmethod
    def calculate_percentage(value) -> float | None:
        if FaceVerifier.THREASHOLD <= value:
            percentage = (value - FaceVerifier.THREASHOLD) * 100
            return percentage
        elif 0 <= value < FaceVerifier.THREASHOLD:
            percentage = (value - FaceVerifier.THREASHOLD) / FaceVerifier.THREASHOLD * 100
            return percentage
        else:
            return None
    
    @staticmethod
    def get_embeddings(image_url):
      image = dlib.load_rgb_image(image_url)
      
      faces = FaceVerifier.cv2_face_detection(image_url)
      if len(faces) < 1:
        print("No face detected")
        return
      elif len(faces)> 1:
        print("More than one face")
        return
      else:
        face = faces[0]
        try:
            face.left()
        except:
            face = face.rect
        
        shape = FaceVerifier.sp(image, face)
        face_descriptor = FaceVerifier.facerec.compute_face_descriptor(image, shape)
        face_embedding = np.array(face_descriptor)
        return face_embedding
    
    @staticmethod
    def preprocess_face(face_bbox) -> tuple[int] | None:
        x, y, w, h = face_bbox
        
        left_crop_percentage = 0.1
        right_crop_percentage = 0.1
        top_crop_percentage = 0
        bottom_crop_percentage = 0
        
        left_crop = int(left_crop_percentage * w)
        right_crop = int(right_crop_percentage * w)
        top_crop = int(top_crop_percentage * h)
        bottom_crop = int(bottom_crop_percentage * h)
        
        new_x = max(0, x + left_crop)
        new_y = max(0, y + top_crop)
        new_w = max(0, w - left_crop - right_crop)
        new_h = max(0, h - top_crop - bottom_crop)
    
        adjusted_face_bbox = (new_x, new_y, new_w, new_h)
        return adjusted_face_bbox
    
    @staticmethod
    def cv2_face_detection(img_url) -> list[dlib.rectangle] | None:
        img = cv2.imread(img_url)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = FaceVerifier.face_cascade.detectMultiScale(gray, 1.3, 10)
        out = []
        for f in faces:
            x,y,w,h = FaceVerifier.preprocess_face(f)
            face = dlib.rectangle(x,y,x+w,y+h)
            out.append(face)
            left, top, right, bottom = (face.left(), face.top(), face.right(), face.bottom())
            cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 2)
        return out