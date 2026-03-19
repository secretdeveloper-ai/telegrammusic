import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.mongo_group_manager import MongoGroupManager

logger = logging.getLogger(__name__)
group_manager = MongoGroupManager()


async def init_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initialize group settings"""
    group_id = update.effective_chat.id
    group_name = update.effective_chat.title or "Unknown"

    settings = await group_manager.initialize_group(group_id, group_name)
    info = await group_manager.get_group_info(group_id)
    await update.message.reply_text(
        f"✅ Group initialized!\n\n{info}",
        parse_mode="Markdown"
    )


async def group_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display group information"""
    group_id = update.effective_chat.id
    info = await group_manager.get_group_info(group_id)
    await update.message.reply_text(info, parse_mode="Markdown")


async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add user as admin"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/admin_add <user_id>`",
            parse_mode="Markdown"
        )
        return

    try:
        user_id = int(context.args[0])
        group_id = update.effective_chat.id
        requester_id = update.effective_user.id

        # Check if requester is admin
        is_admin = await group_manager.is_admin(group_id, requester_id)
        if not is_admin and requester_id != update.effective_chat.id:
            await update.message.reply_text("❌ Only admins can add admins!")
            return

        if await group_manager.add_admin(group_id, user_id):
            await update.message.reply_text(f"✅ User {user_id} is now admin!")
        else:
            await update.message.reply_text(f"⚠️ User {user_id} is already admin!")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID!")


async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove admin"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/admin_remove <user_id>`",
            parse_mode="Markdown"
        )
        return

    try:
        user_id = int(context.args[0])
        group_id = update.effective_chat.id
        requester_id = update.effective_user.id

        # Check if requester is admin
        is_admin = await group_manager.is_admin(group_id, requester_id)
        if not is_admin:
            await update.message.reply_text("❌ Only admins can remove admins!")
            return

        if await group_manager.remove_admin(group_id, user_id):
            await update.message.reply_text(f"✅ User {user_id} is no longer admin!")
        else:
            await update.message.reply_text(f"⚠️ User {user_id} is not an admin!")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID!")


async def ban_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban user from group"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/ban <user_id>`",
            parse_mode="Markdown"
        )
        return

    try:
        user_id = int(context.args[0])
        group_id = update.effective_chat.id
        requester_id = update.effective_user.id

        # Check if requester is admin
        is_admin = await group_manager.is_admin(group_id, requester_id)
        if not is_admin:
            await update.message.reply_text("❌ Only admins can ban users!")
            return

        if await group_manager.ban_user(group_id, user_id):
            await update.message.reply_text(f"🚫 User {user_id} is now banned!")
        else:
            await update.message.reply_text(f"⚠️ User {user_id} is already banned!")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID!")


async def unban_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban user"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/unban <user_id>`",
            parse_mode="Markdown"
        )
        return

    try:
        user_id = int(context.args[0])
        group_id = update.effective_chat.id
        requester_id = update.effective_user.id

        # Check if requester is admin
        is_admin = await group_manager.is_admin(group_id, requester_id)
        if not is_admin:
            await update.message.reply_text("❌ Only admins can unban users!")
            return

        if await group_manager.unban_user(group_id, user_id):
            await update.message.reply_text(f"✅ User {user_id} is now unbanned!")
        else:
            await update.message.reply_text(f"⚠️ User {user_id} is not banned!")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID!")


async def set_prefix_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set command prefix for group"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/set_prefix <prefix>`\n"
            "Example: `/set_prefix !`",
            parse_mode="Markdown"
        )
        return

    prefix = context.args[0]
    group_id = update.effective_chat.id
    requester_id = update.effective_user.id

    # Check if requester is admin
    is_admin = await group_manager.is_admin(group_id, requester_id)
    if not is_admin:
        await update.message.reply_text("❌ Only admins can change prefix!")
        return

    if await group_manager.set_prefix(group_id, prefix):
        await update.message.reply_text(f"✅ Prefix changed to: `{prefix}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Could not change prefix!")


async def set_queue_limit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set queue limit"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/queue_limit <number>`\n"
            "Example: `/queue_limit 100`",
            parse_mode="Markdown"
        )
        return

    try:
        limit = int(context.args[0])
        group_id = update.effective_chat.id
        requester_id = update.effective_user.id

        # Check if requester is admin
        is_admin = await group_manager.is_admin(group_id, requester_id)
        if not is_admin:
            await update.message.reply_text("❌ Only admins can change queue limit!")
            return

        if await group_manager.set_queue_limit(group_id, limit):
            await update.message.reply_text(f"✅ Queue limit set to: `{limit}`", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Queue limit must be between 1 and 100!")
    except ValueError:
        await update.message.reply_text("❌ Invalid number!")

