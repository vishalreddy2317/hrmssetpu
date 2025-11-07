"""
FAQ Model
Frequently Asked Questions management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class FAQ(BaseModel):
    """
    Frequently Asked Questions model
    """
    
    __tablename__ = "faqs"
    
    # Question and Answer
    question: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Category
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="general, appointments, billing, services, emergency, insurance, pharmacy, lab, technical"
    )
    
    # Subcategory (optional)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100), comment="Specific subcategory")
    
    # Display Order
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Tags
    tags: Mapped[Optional[str]] = mapped_column(String(500), comment="Comma-separated tags for search")
    keywords: Mapped[Optional[str]] = mapped_column(String(500), comment="Search keywords")
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='published',
        nullable=False,
        index=True,
        comment="draft, published, archived, under_review"
    )
    
    # Visibility
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, comment="Featured on homepage")
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, comment="Visible to public")
    
    # View Statistics
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_viewed_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Feedback/Rating
    helpful_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    not_helpful_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer, comment="Average rating 1-5")
    
    # Language
    language: Mapped[str] = mapped_column(String(10), default='en', nullable=False)
    
    # Related FAQs
    related_faqs: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of FAQ IDs")
    
    # Rich Content
    answer_html: Mapped[Optional[str]] = mapped_column(Text, comment="HTML formatted answer")
    attachments: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of attachment URLs")
    video_url: Mapped[Optional[str]] = mapped_column(String(500), comment="Tutorial video URL")
    
    # Metadata
    author: Mapped[Optional[str]] = mapped_column(String(200), comment="FAQ author")
    created_by: Mapped[Optional[str]] = mapped_column(String(200))
    last_updated_by: Mapped[Optional[str]] = mapped_column(String(200))
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(200))
    reviewed_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Publishing
    published_date: Mapped[Optional[str]] = mapped_column(String(20))
    expires_at: Mapped[Optional[str]] = mapped_column(String(20), comment="Auto-archive date")
    
    # SEO
    meta_title: Mapped[Optional[str]] = mapped_column(String(200), comment="SEO meta title")
    meta_description: Mapped[Optional[str]] = mapped_column(String(500), comment="SEO meta description")
    slug: Mapped[Optional[str]] = mapped_column(String(500), unique=True, comment="URL-friendly slug")
    
    # Version Control
    version: Mapped[int] = mapped_column(Integer, default=1, comment="Version number")
    previous_version_id: Mapped[Optional[int]] = mapped_column(Integer, comment="Previous version FAQ ID")
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text, comment="Internal notes")
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('view_count >= 0', name='faq_positive_view_count'),
        CheckConstraint('helpful_count >= 0', name='faq_positive_helpful_count'),
        CheckConstraint('not_helpful_count >= 0', name='faq_positive_not_helpful_count'),
        CheckConstraint('rating >= 1 AND rating <= 5 OR rating IS NULL', name='faq_valid_rating'),
        CheckConstraint('display_order >= 0', name='faq_positive_display_order'),
        Index('idx_faq_category_status', 'category', 'status'),
        Index('idx_faq_order', 'display_order', 'status'),
        Index('idx_faq_featured', 'is_featured', 'status'),
        Index('idx_faq_language', 'language', 'status'),
        Index('idx_faq_published', 'published_date', 'status'),
        {'comment': 'Frequently Asked Questions management'}
    )
    
    # Validators
    @validates('category')
    def validate_category(self, key, value):
        valid_categories = [
            'general', 'appointments', 'billing', 'services',
            'emergency', 'insurance', 'pharmacy', 'lab', 
            'technical', 'medical', 'departments', 'facilities'
        ]
        if value.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['draft', 'published', 'archived', 'under_review']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('language')
    def validate_language(self, key, value):
        valid_languages = ['en', 'es', 'fr', 'de', 'zh', 'ar', 'hi', 'pt', 'ru', 'ja']
        if value.lower() not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        return value.lower()
    
    @validates('rating')
    def validate_rating(self, key, value):
        if value is not None and (value < 1 or value > 5):
            raise ValueError("Rating must be between 1 and 5")
        return value
    
    def __repr__(self) -> str:
        return f"<FAQ(id={self.id}, question='{self.question[:50]}...', category='{self.category}')>"
    
    # Helper Methods
    def calculate_helpfulness_score(self) -> float:
        """Calculate helpfulness percentage"""
        total = self.helpful_count + self.not_helpful_count
        if total == 0:
            return 0.0
        return round((self.helpful_count / total) * 100, 2)
    
    def is_popular(self) -> bool:
        """Check if FAQ is popular (>100 views)"""
        return self.view_count > 100
    
    def increment_view(self):
        """Increment view count"""
        self.view_count += 1
        from datetime import datetime
        self.last_viewed_at = datetime.utcnow().isoformat()
    
    def mark_helpful(self):
        """Mark as helpful"""
        self.helpful_count += 1
    
    def mark_not_helpful(self):
        """Mark as not helpful"""
        self.not_helpful_count += 1