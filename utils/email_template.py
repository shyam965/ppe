import os



# def verification_mail(name, email, message):
#     return f"""
#     <html>
#         <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; padding: 20px;">
#             <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
#                 <h2 style="color: #007bff; text-align: center;">Welcome to SKILL KRONOS</h2>
#                 <p>Dear <strong>{name}</strong>,</p>
#                 <p>Thank you for reaching out to us!</p>
#                 <p><strong>Your Email:</strong> {email}</p>
#                 <p><strong>Your Message:</strong></p>
#                 <blockquote style="border-left: 4px solid #007bff; padding-left: 10px; color: #555;">
#                     {message}
#                 </blockquote>
#                 <p>We appreciate your interest and will get back to you soon.</p>
#                 <br>
#                 <p>Best regards,</p>
#                 <p><strong>SKILL KRONOS Team</strong></p>
#             </div>
#         </body>
#     </html>
#     """


# def course_published_email(mentor_name, course_title):
   
#     return f"""
#     <html>
#         <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
#             <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px #ddd;">
#                 <h3 style="text-align: center;">Welcome to SKILL KRONOS</h3>
#                 <p>Dear {mentor_name},</p>
#                 <p>We are excited to inform you that your course "<strong>{course_title}</strong>" has been successfully published on <strong>SKILL KRONOS</strong>.</p>
                
#                 <p>Now, students can enroll and start learning from your course.</p>
                
               

#                 <p>We appreciate your contribution to our platform and wish you great success with your course!</p>

#                 <p>Best regards,</p>
#                 <p><strong>SKILL KRONOS Team</strong></p>
#             </div>
#         </body>
#     </html>
#     """

# def generate_meeting_email_template(first_name,date,time, meeting_link):
    
    
#     return f"""
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         </head>
#         <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5; color: #333333;">
#             <div style="max-width: 600px; margin: 40px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
#                 <!-- Header -->
#                 <div style="background-color: #1a365d; padding: 30px 40px; text-align: center;">
#                     <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;">Welcome to Skill Kronos</h1>
#                 </div>

                

#                 <!-- Content -->
#                 <div style="padding: 40px; background-color: #ffffff;">
#                     <p style="margin-top: 0; margin-bottom: 16px; font-size: 16px; line-height: 1.6;">Dear {first_name},</p>
                    
#                     <p style="margin-bottom: 20px; font-size: 16px; line-height: 1.6;">
#                         A mentor from our platform has scheduled a mentoring session with you. We're excited to facilitate this valuable connection!
#                     </p>

#                     <!-- Scheduled Date & Time -->
#                     <div style="background-color: #eef2ff; padding: 15px; text-align: center; border-radius: 8px; margin-bottom: 20px;">
#                         <p style="margin: 0; font-size: 16px; font-weight: bold; color: #1a365d;">
#                             📅 Scheduled Date & Time: {date} & {time}
#                         </p>
#                     </div>
                    
#                     <!-- Meeting Link Box -->
#                     <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; margin: 30px 0; text-align: center;">
#                         <p style="margin-bottom: 20px; font-size: 16px; color: #4a5568;">
#                             Click the button below to join your scheduled meeting:
#                         </p>
#                         <a href="{meeting_link}" 
#                            style="display: inline-block; padding: 14px 32px; background-color: #2563eb; color: #ffffff; text-decoration: none; font-weight: 600; border-radius: 6px; font-size: 16px; transition: background-color 0.3s ease;">
#                             Join Meeting
#                         </a>
#                     </div>
                    
#                     <!-- Important Notes -->
#                     <div style="margin-top: 30px; padding: 20px; background-color: #fff7ed; border-left: 4px solid #fb923c; border-radius: 4px;">
#                         <p style="margin: 0; font-size: 15px; color: #666666; line-height: 1.6;">
#                             <strong style="color: #333333;">Important:</strong> Please ensure you have a stable internet connection and your audio/video devices are working properly before joining the meeting.
#                         </p>
#                     </div>
                    
#                     <p style="margin-top: 30px; margin-bottom: 8px; font-size: 16px; line-height: 1.6;">
#                         If you have any questions or need technical assistance, please don't hesitate to contact our support team.
#                     </p>
                    
#                     <p style="margin-top: 30px; margin-bottom: 8px; font-size: 16px; line-height: 1.6;">Best regards,</p>
#                     <p style="margin-top: 0; margin-bottom: 0; font-size: 16px; font-weight: 600; color: #1a365d;">SKILL KRONOS Team</p>
#                 </div>
                
#                 <!-- Footer -->
#                 <div style="background-color: #f8fafc; padding: 20px 40px; text-align: center; border-top: 1px solid #e2e8f0;">
#                     <p style="margin: 0; font-size: 14px; color: #64748b;">
#                         © 2025 SKILL KRONOS. All rights reserved.
#                     </p>
#                 </div>
#             </div>
#         </body>
#     </html>
#     """


# def generate_contact_mentor_email_template(mentor_name, user_email):
#     return f"""
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         </head>
#         <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5; color: #333333;">
#             <div style="max-width: 600px; margin: 40px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
#                 <!-- Header -->
#                 <div style="background-color: #1a365d; padding: 30px 40px; text-align: center;">
#                     <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;">Welcome to Skill Kronos</h1>
#                 </div>

#                 <!-- Content -->
#                 <div style="padding: 40px; background-color: #ffffff;">
#                     <p style="margin-top: 0; margin-bottom: 16px; font-size: 16px; line-height: 1.6;">Dear {mentor_name},</p>
                    
#                     <p style="margin-bottom: 20px; font-size: 16px; line-height: 1.6;">
#                         A user is interested in connecting with you for mentorship.
#                     </p>

#                     <!-- User Contact Info -->
#                     <div style="background-color: #eef2ff; padding: 15px; text-align: center; border-radius: 8px; margin-bottom: 20px;">
#                         <p style="margin: 0; font-size: 16px; font-weight: bold; color: #1a365d;">
#                             📧 Contact Email: {user_email}
#                         </p>
#                     </div>
                    
#                     <p style="margin-top: 30px; margin-bottom: 8px; font-size: 16px; line-height: 1.6;">
#                         Please feel free to reach out to the user at your convenience.
#                     </p>
                    
#                     <p style="margin-top: 30px; margin-bottom: 8px; font-size: 16px; line-height: 1.6;">Best regards,</p>
#                     <p style="margin-top: 0; margin-bottom: 0; font-size: 16px; font-weight: 600; color: #1a365d;">SKILL KRONOS Team</p>
#                 </div>
                
#                 <!-- Footer -->
#                 <div style="background-color: #f8fafc; padding: 20px 40px; text-align: center; border-top: 1px solid #e2e8f0;">
#                     <p style="margin: 0; font-size: 14px; color: #64748b;">
#                         © 2024 SKILL KRONOS. All rights reserved.
#                     </p>
#                 </div>
#             </div>
#         </body>
#     </html>
#     """




# <!-- Image Centered -->
#                 <div style="text-align: center; padding: 20px;">
#                     <img src="	https://www.techasoft.com/blog/2021/01/1609606508.png" 
#                          alt="Meeting Image" 
#                          style="max-width: 100%; height: auto; border-radius: 8px;">
#                 </div>



 # <div style="text-align: center; margin: 20px 0;">
                #     <a href="https://www.skillkronos.com/courses/{course_title.replace(' ', '-').lower()}" 
                #     style="background-color: #3498db; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                #         View Your Course
                #     </a>
                # </div>

# def Verification_mail(name, id):
#     return f"""
# <img src="https://www.skillkronos.com/skillkronos_logo.png" width="100px" alt="skillkronos Logo" style="display: block; margin: 0 auto;">
# Dear {name},
# <br>
# Thank you for signing up with SKILL KRONOS. To complete the registration process and ensure the security of your account, we kindly ask you to verify your email address.
# <br>
# Please click on the following link to verify your email:
# <br>
# <a href="{os.environ.get("FRONTEND_URL")}/password/{id}">Click Here</a>
# <br>
# If the link above is not clickable, you can copy and paste it into your browser's address bar.
# <br>
# If you did not create an account with SKILL KRONOS, please disregard this email. Your information remains secure, and no further action is required.
# <br>
# Thank you for choosing SKILL KRONOS. If you encounter any issues or have questions, please contact our support team at
# <br>
# Best regards,
# <br>
# SKILL KRONOS"""
